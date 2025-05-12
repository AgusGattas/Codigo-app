import json
from typing import List

from pydantic import BaseModel, Field, validate_call

from app.core.config import settings
from app.database.mixins import OrmBaseModel
from app.modules.talent.experience.schemas import ExperienceResponse
from app.modules.talent.models import Talent

from .external_api_service import ExternalApiService


class User(OrmBaseModel):
    first_name: str = ""
    last_name: str = ""


class Resume(OrmBaseModel):
    summary: str = ""
    user: User = User()
    job_history: List[ExperienceResponse] = Field(default=[], alias="experiences")
    academic_history: List[dict] = []
    main_skills: List[str] = []
    languages: List[dict] = []
    certifications: List[dict] = []


class Document(BaseModel):
    resume: Resume


class TalentEchoService(ExternalApiService):
    base_url: str = settings.TALENT_ECHO_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    def create(self, talent: Talent):
        data = {
            "talent_id": str(talent.id),
            "documents": [{"resume": json.loads(Resume.model_validate(talent).model_dump_json())}],
        }
        return self.post(endpoint="/TalentEchoCreator", json=data)


class RedFlagsService(ExternalApiService):
    base_url: str = settings.TALENT_RED_FLAGS_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    @validate_call(validate_return=True)
    def get_red_flags(
        self, talent_experiences: List[ExperienceResponse], open_to_work: bool
    ) -> List[str]:
        data = {
            "job_history": [json.loads(exp.model_dump_json()) for exp in talent_experiences],
            "open_to_work": str(open_to_work),
        }
        return self.post(endpoint="/candidate_flycheck/candididate_flycheck", json=data)[
            "flycheck_output"
        ]
