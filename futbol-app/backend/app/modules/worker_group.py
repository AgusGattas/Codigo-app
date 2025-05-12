import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from typing import Callable, Tuple

from fastapi_injector.request_scope import _request_id_ctx
from injector import Inject

from app.context import fork_request_context, get_request_context
from app.database.base import DatabaseResource
from app.dependencies import RequestContext


class WorkerException(Exception):
    def __init__(self, exc):
        self.exc = exc
        self.thread_id = threading.get_ident()

    def __repr__(self) -> str:
        return f"WorkerException(thread_id={self.thread_id}, exc={self.exc!r})"


class ParallelService:
    def __init__(self, db: Inject[DatabaseResource]):
        self.db = db

    def worker_group(self, max_threads=20, track_time=False, name="Worker Group"):
        return WorkerGroup(self.db, max_threads, track_time, name)


class WorkerGroup:
    def __init__(self, db: DatabaseResource, max_threads: int, track_time: bool, name: str):
        self.max_threads = max_threads
        self.track_time = track_time
        self.name = name

        self.tasks = Queue()
        self.exceptions = []
        self.executor = ThreadPoolExecutor(max_workers=max_threads)
        self.task_times = []

        self.db = db

    def add_task(self, fn: Callable, *args, **kwargs):
        self.tasks.put((fn, args, kwargs))

    def worker(self, fn: Callable, args: Tuple, kwargs: dict, req_ctx: RequestContext):
        """Executes a task, handling timing, exceptions, and stats."""
        start_time = time.time() if self.track_time else None
        thread_id = threading.get_ident()

        _request_id_ctx.set(thread_id)
        fork_request_context(req_ctx)

        try:
            print(f"Running {fn.__name__}")
            fn(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            self.db.session.remove()

            if self.track_time:
                elapsed = time.time() - start_time
                self.task_times.append(
                    {
                        "fn_name": fn,
                        "thread_id": thread_id,
                        "args": args,
                        "elapsed_time": elapsed,
                    }
                )

    def run_tasks(self):
        """Run all tasks in the queue up to the max_threads limit."""
        futures = []
        while not self.tasks.empty():
            fn, args, kwargs = self.tasks.get()
            req_ctx = get_request_context()
            futures.append(self.executor.submit(self.worker, fn, args, kwargs, req_ctx))

        if self.track_time:
            start_time = time.time()

        for future in as_completed(futures):
            future.result()  # raises any exceptions, handled by worker

        if self.track_time:
            total_time = time.time() - start_time
            self._print_stats(total_time)

    def join(self):
        """Runs all tasks and waits for completion, raising exceptions if any occurred."""
        self.run_tasks()
        self.executor.shutdown(wait=True)
        if self.exceptions:
            raise WorkerException("Exceptions occurred in worker tasks:", self.exceptions)

    def _print_stats(self, total_time: float):
        """Prints timing statistics for all tasks and the total duration of the worker group."""
        print(f"\n`{self.name}` Statistics:")
        for stat in self.task_times:
            print(
                f"\t\tfn: {stat['fn_name']}, tid: {stat['thread_id']}, "
                f"time: {stat['elapsed_time']:.4f} seconds"
            )
        print(f"\tTotal Time for `{self.name}`: {total_time:.4f} seconds\n")
