from typing import List

from fastapi import UploadFile
from loguru import logger
from pydantic import ValidationError, validate_call

from app.core.config import settings
from app.modules.export.schemas import TalentExport, TalentTailoredData
from app.modules.talent.schemas import (
    PartialTalentResumeParserResponse,
    PartialWorkExperience,
)
from app.services.exceptions import ExternalApiException

from .external_api_service import ExternalApiService


class InvalidResumeFileError(ExternalApiException):
    status_code = 400
    detail = "The uploaded resume file is invalid. Please upload a valid resume file."


class TailorResumeException(ExternalApiException):
    status_code = 400
    detail = "Error occurred while tailoring resume."


class CoreSkillsException(ExternalApiException):
    status_code = 400
    detail = "Error occurred while extracting core skills."


class ResumeParserService(ExternalApiService):
    base_url: str = settings.RESUME_PARSER_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    def to_dict(self, resume: UploadFile) -> PartialTalentResumeParserResponse:
        @validate_call(validate_return=True)
        def __to_dict(self, resume: UploadFile) -> PartialTalentResumeParserResponse:
            files = {"file": (resume.filename, resume.file.read(), resume.content_type)}
            try:
                return self.post(endpoint="/TalentParser/resume_file_to_json/", files=files)[
                    "parsed_resume"
                ]
            except ExternalApiException as e:
                error_message = e.detail[0]["msg"]
                raise InvalidResumeFileError(detail=error_message) from e

        try:
            return __to_dict(self, resume)
        except ValidationError as e:
            logger.error(f"Error parsing resume filename[{resume.filename}]: {e}")
            raise InvalidResumeFileError(
                detail="We couldn't parse your resume. Make sure its content is in English and the dates are correctly formatted."
            ) from e

    @validate_call(validate_return=True)
    def tailor_resume(
        self, talent: TalentExport, job_description: str, job_title: str = ""
    ) -> TalentTailoredData:
        try:
            return self.post(
                endpoint="/tailored_resume/tailor",
                json={
                    "candidate_desc": talent.model_dump(),
                    "job_description": {
                        "job_title": job_title,
                        "job_description": job_description,
                    },
                },
            )
        except ExternalApiException as e:
            raise TailorResumeException from e

    @validate_call(validate_return=True)
    def extract_talent_core_skills(
        self, summary: str, work_experience: List[PartialWorkExperience]
    ) -> List[str]:
        try:
            return self.post(
                endpoint="/TalentParser/core_skills/",
                json={
                    "summary": summary,
                    "work_experiences": [exp.model_dump() for exp in work_experience],
                },
            )["core_skills"]
        except ExternalApiException as e:
            raise CoreSkillsException from e

    @validate_call(validate_return=True)
    def get_summary(self, experience: List[PartialWorkExperience]) -> str:
        return self.post(
            endpoint="/TalentParser/summary/",
            json={"experience": [exp.model_dump() for exp in experience]},
        )["summary"]
