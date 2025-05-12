import uuid
from datetime import datetime
from typing import List

from loguru import logger
from pydantic import Field, validate_call

from app.core.config import settings
from app.database.mixins import OrmBaseModel
from app.modules.contact.job.schemas import JobBase
from app.modules.contact.relationship.schemas import RelationshipType
from app.modules.contact.schemas import ContactBase
from app.services.exceptions import ExternalApiException
from app.services.external_api_service import ExternalApiService


class UserProfileNameOnly(OrmBaseModel):
    full_name: str = ""


class CompanyNameOnly(OrmBaseModel):
    name: str


class RelationshipEchoSchema(OrmBaseModel):
    type: RelationshipType | None = None
    notes: str | None = ""
    start_date: datetime | None = None
    end_date: datetime | None = None
    role: str = ""
    contacted_by: UserProfileNameOnly | None = None
    company: CompanyNameOnly | None = None
    job_orders_count: int | None = None
    send_outs_count: int | None = None
    placements_count: int | None = None
    client_visits_count: int | None = None


class JobEchoSchema(OrmBaseModel, JobBase):
    company: CompanyNameOnly


class InteractionEchoSchema(OrmBaseModel):
    type: str | None = None
    description: str | None = ""
    date: datetime | None = None
    data: dict = {}
    created_by: UserProfileNameOnly | None = None
    updated_by: UserProfileNameOnly | None = None
    client_visits_count: int | None = None
    job_orders_count: int | None = None
    send_outs_count: int | None = None
    placements_count: int | None = None


class ContactEchoSchema(OrmBaseModel, ContactBase):
    id: uuid.UUID
    jobs: List[JobEchoSchema] = []
    relationships: List[RelationshipEchoSchema] = []
    interactions: List[InteractionEchoSchema] = []


class ContactEchoService(ExternalApiService):
    base_url: str = settings.CONTACT_ECHO_CREATOR_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    @validate_call
    def upsert(self, contact: ContactEchoSchema):
        ## Only train the contact echo if they have at least one job, one relationship or one interaction
        if any([contact.jobs, contact.relationships, contact.interactions]):
            contact = contact.model_dump(mode="json")

            contact_data = {
                "jobs": contact["jobs"],
                "activities": contact["relationships"],
                "interactions": contact["interactions"],
            }

            data = {
                "entity_id": str(contact["id"]),
                "entity": "contact",
                "documents": [
                    {
                        "resume": {
                            "first_name": contact["first_name"],
                            "last_name": contact["last_name"],
                            "linkedin_url": contact["linkedin"],
                            "academic_history": contact["education"],
                            "email": contact["email"],
                            "phone": contact["phone"],
                            "linkedin": contact["linkedin"],
                        },
                        **contact_data,
                    }
                ],
            }

            return self.post(endpoint="/EntityEchoCreator", json=data)


class ContactTrackingPayload(OrmBaseModel):
    contact_first_name: str = Field("", alias="first_name")
    contact_last_name: str = Field("", alias="last_name")
    linkedin_url: str = Field(default="", alias="linkedin")
    company: str = ""
    is_prospect: bool = True
    contact_id: uuid.UUID = Field(alias="id")
    tenant_id: uuid.UUID = ""
    kforce_external_id: str | None = ""
    ## Add every external id to the payload


class ContactTrackingAPI(ExternalApiService):
    base_url: str = settings.CONTACT_TRACKING_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    @validate_call
    def track_contact(self, contact: ContactTrackingPayload):
        return self.post(
            endpoint="/contacts_input/contacts_input_profiles", json=contact.model_dump(mode="json")
        )

    @validate_call
    def track_contacts(self, contacts: list[ContactTrackingPayload]):
        return self.post(
            endpoint="/contacts_input/add_contacts_bulk",
            json={"contacts": [contact.model_dump(mode="json") for contact in contacts]},
        )

    @validate_call
    def stop_tracking_contact(self, contact_id: uuid.UUID):
        return self.patch(
            endpoint="/contacts_input/update_contact",
            json={"contact_id": str(contact_id), "to_scrape": False},
        )

    @validate_call
    def update_tracking_contact(self, contact_id: uuid.UUID, linkedin_url: str):
        try:
            return self.patch(
                endpoint="/contacts_input/update_contact",
                json={"contact_id": str(contact_id), "linkedin_url": linkedin_url},
            )
        except ExternalApiException as e:
            logger.error(f"Error updating a contact linkedin url: {e}")
