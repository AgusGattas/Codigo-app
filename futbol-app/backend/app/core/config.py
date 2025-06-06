"""Configuration to use in the app"""

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Union, Optional

NoSchemaNone = SkipJsonSchema[
    None
]  # TODO remove after this PR is merged https://github.com/tiangolo/fastapi/pull/9873


class CommonSettings(BaseSettings):
    APP_NAME: str = Field(default="Echo-backend")
    DEBUG_MODE: bool = Field(default=False)
    MAX_ALLOWED_MATCHES: int = Field(default=50)
    ENVIRONMENT: str = Field(default="local")

    ENABLE_ACCESS_CONTROL: bool = Field(default=False)


class DatabaseSettings(BaseSettings):
    DB_NAME: str = Field(default="echo-backend")
    DB_URL: str = Field(default="sqlite:///sql.db")
    DB_POOL_SIZE: int = Field(default=30)
    DB_POOL_PRE_PING: bool = Field(default=False)
    REPOSITORY_NAME: str = Field(default="SQL")  ## For the new entities
    POOL_RECYCLE_MINUTES: int = Field(default=10)

    DB_ADMIN_ROLE: str = Field(default="postgres")
    DB_AUTH_ROLE: str = Field(default="echo_backend")
    DB_STATEMENT_TIMEOUT_MS: int = Field(default=20000)


class CORSSettings(BaseSettings):
    FRONTEND_URL: str = Field(default="http://localhost:3000")


class ExternalServicesApiSettings(BaseSettings):
    VECTORIZER_API_URL: str = "https://matching-products-api.taller.ai"
    MATCHING_DIFF_API_URL: str = "https://matching-diff-api-dev.taller.ai"
    TALENT_ECHO_API_URL: str = "https://talent-echo-creator-dev.taller.ai"
    RESUME_PARSER_API_URL: str = "https://resume-parser-dev.taller.ai"
    CONTACT_TRACKING_API_URL: str = "https://contacts-input-api-dev.taller.ai"
    ASSESSMENT_CREATOR_API_URL: str = "https://assessment-creator-dev.taller.ai"
    GRAMMAR_CHECKER_API_URL: str = "https://grammar-checker-dev.taller.ai"
    PROJECT_TEAM_BUILDER_API_URL: str = "https://team-builder-dev.taller.ai"
    ECHO_DOCUMENT_API_URL: str = "https://free-document-loader-dev.taller.ai"
    MERGE_TOOL_API_URL: str = "https://merge-tool-api-dev.taller.ai"
    TALENT_RED_FLAGS_API_URL: str = "https://echo-candidates-flycheck-api-dev.taller.ai"
    CONTACT_ECHO_CREATOR_API_URL: str = "https://echo-chat-create-contacts-api-dev.taller.ai"
    ORGANIZATION_TRACKING_API_URL: str = "https://scrapers-inputs-api-kforce.taller.ai"
    SQL_QUERY_BUILDER_API_URL: str = "https://smart-search-dev.taller.ai"


class CredentialsSettings(BaseSettings):
    """Google credentials to use in the app
    to connect to Firestore and other services"""

    ECHO_INTERNAL_API_KEY: str = "replace-me-echo-internal-api-key"
    ECHO_API_SIGNATURE_KEY: str = "replace-me-echo-signature"

    AUTH_JWT_SECRET: str = ""

    AXIOM_API_KEY: str = ""
    AXIOM_ORG_ID: str = ""
    AXIOM_DATASET_NAME: str = "echo-backend"
    SUPABASE_URL: str
    SUPABASE_PRIVATE_KEY: str

    SENTRY_DSN: str
    SENTRY_TRACES_SAMPLE_RATE: float = 0.0
    SENTRY_PROFILES_SAMPLE_RATE: float = 0.0


class AWSSettings(BaseSettings):
    ASSETS_BUCKET: str = "taller-echo"
    # AWS_ACCESS_KEY_ID: str | None = None ## Forbidden variables for AWS Services (since you should use role based permissions)
    # AWS_SECRET_ACCESS_KEY: str | None = None
    S3_ACCESS_KEY_ID: Optional[str] = None
    S3_SECRET_ACCESS_KEY: Optional[str] = None
    S3_BUCKET_NAME: Optional[str] = None
    S3_REGION: Optional[str] = None
    REGION_NAME: str = "us-east-1"
    ENDPOINT_URL: Optional[str] = None
    CDN_URL: str = "https://d1a324xj07l38i.cloudfront.net"


class EchoSettings(BaseSettings):
    TALENT_SEMANTIC_SEARCH_THRESHOLD: int = Field(
        default=10, description="Threshold for the semantic search of talents. 0 means no threshold"
    )


class Settings(
    CommonSettings,
    CredentialsSettings,
    AWSSettings,
    DatabaseSettings,
    EchoSettings,
    ExternalServicesApiSettings,
    CORSSettings,
):
    PROJECT_NAME: str = "Futbol App"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DB_URL: str = "postgresql://postgres:postgres@localhost:5432/futbol"
    DB_POOL_SIZE: int = 5
    
    # Repository
    REPOSITORY_NAME: str = "SQL"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
