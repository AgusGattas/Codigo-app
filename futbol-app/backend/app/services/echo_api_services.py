from pydantic import BaseModel, computed_field, validate_call

from app.core.config import settings
from app.services.external_api_service import ExternalApiService


class EchoDocument(BaseModel):
    echo_entity: str
    echo_entity_id: str
    file_id: str
    file_type: str
    file_description: str = ""
    file_tag: str = ""
    file_title: str = ""
    process_images: bool = False

    @computed_field
    def file_url(self) -> str:
        return f"{settings.CDN_URL}/{self.file_id}"


class EchoDocumentService(ExternalApiService):
    base_url: str = settings.ECHO_DOCUMENT_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    @validate_call
    def upload_document(self, document: EchoDocument):
        return self.post(endpoint="/documents/upload_file", json=document.model_dump())

    def remove_document(self, echo_entity: str, echo_entity_id: str, file_id: str):
        return self.delete(
            endpoint="/documents/remove_file",
            json={"echo_entity": echo_entity, "echo_entity_id": echo_entity_id, "file_id": file_id},
        )
