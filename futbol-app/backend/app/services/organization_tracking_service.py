import uuid

from pydantic import Field, validate_call

from app.core.config import settings
from app.database.mixins import OrmBaseModel
from app.services.external_api_service import ExternalApiService


class OrganizationTrackingPayload(OrmBaseModel):
    echo_id: uuid.UUID = Field(alias="id")
    name: str = ""
    linkedin_url: str


class OrganizationTrackingAPI(ExternalApiService):
    base_url: str = settings.ORGANIZATION_TRACKING_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    @validate_call(validate_return=True)
    def track_organizations(self, organizations: list[OrganizationTrackingPayload]):
        return self.post(
            endpoint="/companies_inputs/add_companies_bulk",
            json={"companies": [org.model_dump(mode="json") for org in organizations]},
        )

    @validate_call
    def track_organization(self, organization: OrganizationTrackingPayload):
        return self.post(
            endpoint="/companies_inputs/add_company", json=organization.model_dump(mode="json")
        )
