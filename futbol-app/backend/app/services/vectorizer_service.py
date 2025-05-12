import json
import random
from functools import lru_cache
from typing import List

from app.core.config import settings
from app.exceptions import HTTPExceptionMixin

from .external_api_service import ExternalApiService


class TalentVectorizerException(HTTPExceptionMixin):
    status_code = 400
    detail = "Error occurred while vectorizing talent."
    error_code = "talent_vectorizer_error"


class VectorizerService(ExternalApiService):
    base_url: str = settings.VECTORIZER_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    def vectorize_talent(self, summary: str, work_experience: List[dict]) -> List[float]:
        try:
            response = self.post(
                endpoint="/candidates/async_vectorizer_upsert",
                json={"id": 1, "summary": summary or "", "work_experiences": work_experience},
            )
            return json.loads(response["embedding"])
        except Exception as e:
            raise TalentVectorizerException(detail=str(e)) from e

    @lru_cache(maxsize=1000)  # noqa: B019
    def vectorize_job_description(self, job_title: str, job_description: str):
        response = self.post(
            endpoint="/job_descriptions/async_vectorizer_upsert",
            json={"id": 1, "job_title": job_title, "job_description": job_description},
        )
        return json.loads(response["embedding"])

    @lru_cache(maxsize=1000)  # noqa: B019
    def vectorize_text(self, text: str):
        response = self.post(
            endpoint="/semantic_search_candidates/vectorizer",
            json={"search_input": text},
        )
        return json.loads(response["embedding"])


class MockedVectorizerService(VectorizerService):
    def vectorize_talent(self, summary: str, work_experience: List[dict]) -> List[float]:
        return [random.uniform(-0.05, 0.05) for _ in range(1536)]

    def vectorize_job_description(self, job_title: str, job_description: str):
        return [random.uniform(-0.05, 0.05) for _ in range(1536)]
