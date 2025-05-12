import json
from functools import lru_cache
from typing import List

from pydantic import validate_call

from app.core.config import settings
from app.modules.application.schemas import ApplicationMatchDescription, MatchingTechnologies
from app.modules.talent.experience.schemas import ExperienceResponse

from .external_api_service import ExternalApiException, ExternalApiService


class MatchingDiffError(ExternalApiException):
    status_code = 400
    detail = "Matching diff service is currently unavailable"


class MatchingDiffService(ExternalApiService):
    base_url: str = settings.MATCHING_DIFF_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    @validate_call(validate_return=True)
    def get_talent_jd_difference(
        self,
        job_description: str,
        talent_work_experience: List[ExperienceResponse],
        talent_summary: str | None = "",
        job_title: str | None = "",
        technologies: List[str] = [],  # noqa: B006
        nice_to_have_technologies: List[str] = [],  # noqa: B006
        required_technologies: List[str] = [],  # noqa: B006
    ) -> ApplicationMatchDescription:
        payload = json.dumps(
            {
                "candidate_desc": {
                    "id": 1,
                    "summary": talent_summary or "",
                    "work_experiences": [
                        json.loads(exp.model_dump_json()) for exp in talent_work_experience
                    ],
                },
                "job_description": {
                    "id": 1,
                    "job_description": job_description,
                    "job_title": job_title or "",
                },
                "technologies": technologies,
                "nice_to_have": nice_to_have_technologies,
                "required": required_technologies,
            },
        )

        if not technologies:
            return self._do_jd_difference_req(payload, endpoint="/matching_diff/get_matching")
        return self._do_jd_difference_req(payload)

    @lru_cache(maxsize=128)  # noqa: B019
    def _do_jd_difference_req(
        self, body: str, endpoint: str = "/matching_diff/get_matching_and_tech"
    ) -> ApplicationMatchDescription:
        response = self.post(endpoint=endpoint, json=json.loads(body))
        return ApplicationMatchDescription(**response["response"])

    def get_technologies(self, job_title: str = "", job_description: str = "") -> List[str]:
        try:
            return self.post(
                endpoint="/matching_diff/get_technologies",
                json={
                    "job_description": {
                        "job_title": job_title,
                        "job_description": job_description,
                    }
                },
            )["response"]["technologies"]
        except ExternalApiException as e:
            raise MatchingDiffError from e

    @validate_call(validate_return=True)
    def get_technologies_input(
        self, job_title: str = "", job_description: str = ""
    ) -> MatchingTechnologies:
        try:
            return self.post(
                endpoint="/matching_diff/get_technologies",
                json={
                    "job_description": {
                        "job_title": job_title,
                        "job_description": job_description,
                    }
                },
            )["response"]
        except ExternalApiException as e:
            raise MatchingDiffError from e
