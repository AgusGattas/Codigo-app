from contextlib import AsyncExitStack
from typing import Optional, Type, TypeVar

from fastapi import FastAPI
from fastapi_injector import (
    InjectorMiddleware,
    RequestScope,
    RequestScopeOptions,
    attach_injector,
)
from fastapi_injector.exceptions import RequestScopeError
from injector import Injector, InstanceProvider, Provider, ScopeDecorator, singleton
from sqlalchemy import Engine

from app.context import RequestContext, req_or_thread_id
from app.database.base import DatabaseResource, create_sqlalchemy_engine
from app.dependency_registry import registry

T = TypeVar("T")


class RequestOrThreadScope(RequestScope):
    def get(self, key: Type[T], provider: Provider[T]) -> Provider[T]:
        try:
            request_id = req_or_thread_id()
        except LookupError as exc:
            raise RequestScopeError(
                "Request ID missing in cache. "
                "Make sure InjectorMiddleware has been added to the FastAPI instance."
            ) from exc
        stack: Optional[AsyncExitStack] = None

        if request_id not in self.cache:
            self.cache[request_id] = {}

        if self.options.enable_cleanup:
            if AsyncExitStack in self.cache[request_id]:
                stack = self.cache[request_id][AsyncExitStack]
            else:
                stack = self.cache[request_id][AsyncExitStack] = AsyncExitStack()
        if key in self.cache[request_id]:
            dependency = self.cache[request_id][key]
        else:
            dependency = provider.get(self.injector)
            self.cache[request_id][key] = dependency
            if stack:
                self._register(dependency, stack)
        return InstanceProvider(dependency)


class DependencyInjector(Injector):
    """Dependency injector for the app"""

    def __init__(self, db_url: str, pool_size: int = 5) -> None:
        super().__init__()
        self.db_url = db_url
        self.pool_size = pool_size

    def apply_bindings(self):
        """Apply the bindings for the injector. Each class is auto-binded implicitly"""
        # Add SQLAlchemy engine as singleton dependency
        self.binder.bind(
            Engine,
            to=create_sqlalchemy_engine(db_url=self.db_url, pool_size=self.pool_size),
            scope=singleton,
        )

        req_or_thread_scope = RequestOrThreadScope(self)
        self.binder.bind(RequestScope, to=req_or_thread_scope, scope=singleton)
        self.binder.bind(RequestOrThreadScope, to=req_or_thread_scope, scope=singleton)
        request_or_thread_scope = ScopeDecorator(RequestOrThreadScope)

        self.binder.bind(
            DatabaseResource,
            to=DatabaseResource,
            scope=request_or_thread_scope,
        )

        self.binder.bind(
            RequestContext,
            to=RequestContext,
            scope=request_or_thread_scope,
        )

        registry.bind_all(self)

    def setup_injections(self, app: FastAPI):
        """Setup the injections for the app

        Args:
            app (FastAPI): The app to setup the injections for
        """
        self.apply_bindings()
        app.add_middleware(InjectorMiddleware, injector=self)
        options = RequestScopeOptions(enable_cleanup=True)
        attach_injector(app, self, options)
