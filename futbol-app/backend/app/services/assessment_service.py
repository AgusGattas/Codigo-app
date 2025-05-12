import uuid
from math import ceil

from pydantic import BaseModel, Field, computed_field, validate_call

from app.core.config import settings
from app.database.mixins import StrEnum
from app.exceptions import HTTPExceptionMixin

from .external_api_service import ExternalApiService


class AssessmentException(HTTPExceptionMixin):
    status_code = 400
    detail = "Error occurred while getting assessment."
    error_code = "assessment_creation_error"


class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class SkillQuestions(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    skill: str
    questions: list[Question]

    @computed_field
    def technology(self) -> str:
        return self.skill


class InterviewQuestionsResponse(BaseModel):
    must_have: list[SkillQuestions] = []
    nice_to_have: list[SkillQuestions] = []

    @computed_field
    def estimated_duration_minutes(self) -> int:
        total_minutes = sum(3 * len(skill.questions) for skill in self.must_have) + sum(
            1 * len(skill.questions) for skill in self.nice_to_have
        )
        return ceil(total_minutes / 30) * 30


class RegenerationMode(StrEnum):
    COMPLEXIFY = "complexify"
    SIMPLIFY = "simplify"
    REGENERATE = "regenerate"
    GENERATE = "generate"


class InterviewQuestionsRegenerationRequest(BaseModel):
    job_description: str
    question: Question = Field(description="The question to be regenerated")
    regenerate_mode: RegenerationMode
    role_title: str
    skill_context: SkillQuestions = Field(
        description="The skill context to be used for the regeneration. All the questions for the corresponding skill"
    )


class VirtualInterviewQuestionsRegenerationRequest(BaseModel):
    job_description: str
    question: Question = Field(description="The question to be regenerated")
    regenerate_mode: RegenerationMode
    role_title: str
    virtual_interview_questions_context: list[Question] = []

    @computed_field
    def virtual_interview_question(self) -> str:
        return self.question.question


class CodeChallengeResponse(BaseModel):
    live_code_challenge: str = ""
    take_home_code_challenge: str = ""


class RegenerateCodeChallengeRegenerationRequest(BaseModel):
    job_description: str
    code_challenge: str


class AssessmentCreatorService(ExternalApiService):
    base_url: str = settings.ASSESSMENT_CREATOR_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }
    return_json: bool = False

    def create_interview_questions_markdown(self, title: str, job_description: str) -> str:
        try:
            response = self.post(
                endpoint="/markdown_assessment_generator_for_job_description_router",
                json={"job_description_title": title, "job_description": job_description},
            )
            return response.text
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e

    def create_challenge_markdown(self, title: str, job_description: str) -> str:
        try:
            response = self.post(
                endpoint="/markdown_code_challenge_generator_router",
                json={"job_description_title": title, "job_description": job_description},
            )
            return response.text
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e

    def create_virtual_interview_questions_markdown(self, title: str, job_description: str) -> str:
        try:
            response = self.post(
                endpoint="/markdown_virtual_interview_questions_generator",
                json={"job_description_title": title, "job_description": job_description},
            )
            return response.text
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e

    @validate_call(validate_return=True)
    def create_interview_questions(
        self, title: str, job_description: str
    ) -> InterviewQuestionsResponse:
        try:
            return self.post(
                endpoint="/interview_questions_v2",
                json={"role_title": title, "job_description": job_description},
            ).json()["interview_questions"]
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e

    @validate_call(validate_return=True)
    def regenerate_interview_questions(
        self, reg_request: InterviewQuestionsRegenerationRequest
    ) -> Question:
        try:
            return self.post(
                endpoint="/regenerate_interview_question",
                json=reg_request.model_dump(),
            ).json()["question_response"]
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e

    @validate_call(validate_return=True)
    def create_virtual_interview_questions(
        self, title: str, job_description: str
    ) -> list[Question]:
        try:
            return self.post(
                endpoint="/virtual_interview_questions_v2",
                json={"role_title": title, "job_description": job_description},
            ).json()["virtual_interview_questions"]
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e

    @validate_call(validate_return=True)
    def regenerate_virtual_interview_questions(
        self, reg_request: VirtualInterviewQuestionsRegenerationRequest
    ) -> Question:
        try:
            return self.post(
                endpoint="/regenerate_virtual_interview_questions",
                json=reg_request.model_dump(),
            ).json()["virtual_interview_questions"]
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e

    @validate_call(validate_return=True)
    def create_code_challenge(self, title: str, job_description: str) -> CodeChallengeResponse:
        try:
            return self.post(
                endpoint="/code_challenge_v2",
                json={"role_title": title, "job_description": job_description},
            ).json()["code_challenges"]
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e

    @validate_call
    def regenerate_code_challenge(
        self, reg_request: RegenerateCodeChallengeRegenerationRequest
    ) -> str:
        try:
            return self.post(
                endpoint="/regenerate_code_challenge",
                json=reg_request.model_dump(),
            ).json()["regenerated_code_challenge"]
        except Exception as e:
            raise AssessmentException(detail=str(e)) from e


class MockedAssessmentCreatorService(ExternalApiService):
    base_url: str = "fake"

    def create_interview_questions_markdown(self, title: str, job_description: str) -> str:
        return "Mocked Interview Questions"

    def create_challenge_markdown(self, title: str, job_description: str) -> str:
        return "Mocked Challenge"

    def create_virtual_interview_questions_markdown(self, title: str, job_description: str) -> str:
        return "Mocked Virtual Interview Questions"

    def create_interview_questions(
        self, title: str, job_description: str
    ) -> InterviewQuestionsResponse:
        return InterviewQuestionsResponse(
            must_have=[
                SkillQuestions(skill="Python", questions=[Question(question="What is Python?")])
            ],
            nice_to_have=[
                SkillQuestions(skill="Python", questions=[Question(question="What is Python?")])
            ],
        )

    def create_code_challenge(self, title: str, job_description: str) -> CodeChallengeResponse:
        return CodeChallengeResponse(
            live_code_challenge="Mocked live code challenge",
            take_home_code_challenge="Mocked take home code challenge",
        )

    def regenerate_code_challenge(
        self, reg_request: RegenerateCodeChallengeRegenerationRequest
    ) -> str:
        return "Mocked regenerated code challenge"

    def regenerate_interview_questions(
        self, reg_request: InterviewQuestionsRegenerationRequest
    ) -> Question:
        return Question(question="Mocked regenerated interview question")

    def regenerate_virtual_interview_questions(
        self, reg_request: VirtualInterviewQuestionsRegenerationRequest
    ) -> Question:
        return Question(question="Mocked regenerated virtual interview question")

    def create_virtual_interview_questions(
        self, title: str, job_description: str
    ) -> list[Question]:
        return [Question(question="Mocked virtual interview question")]
