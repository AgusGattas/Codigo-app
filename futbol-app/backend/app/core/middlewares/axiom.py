import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Callable

import requests
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class AxiomClient:
    def __init__(self, api_key, dataset_name) -> None:
        self.dataset_name = dataset_name
        self.url = f"https://api.axiom.co/v1/datasets/{dataset_name}/ingest"
        ## Create requests session with the API key as header
        self.session = requests.Session()
        self.session.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def ingest_events(self, events):
        return self.session.post(self.url, json=events)

    def no_response_ingest_events(self, events):
        with ThreadPoolExecutor() as executor:
            executor.submit(self.ingest_events, events)


class AxiomMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = AxiomClient(settings.AXIOM_API_KEY, settings.AXIOM_DATASET_NAME)

    async def dispatch(self, request: Request, call_next: Callable):
        body = {}
        if request.headers.get("Content-Type") == "application/json":
            try:
                body = await request.json()
            except Exception as e:
                print(e)

        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        user_id = getattr(request.state, "user_id", "No Auth")
        user_email = getattr(request.state, "email", "No Auth")
        try:
            self.client.ingest_events(
                events=[
                    {
                        "user_id": user_id,
                        "email": user_email,
                        "environment": settings.ENVIRONMENT,
                        "_time": datetime.now(tz=timezone.utc).isoformat(),
                        "host": request.client.host,
                        "method": request.method,
                        "path": request.url.path,
                        "url": str(request.url),
                        "request_duration": process_time,
                        "body": body,
                        "status_code": response.status_code,
                    }
                ],
            )
        except Exception as e:
            print(e)

        return response
