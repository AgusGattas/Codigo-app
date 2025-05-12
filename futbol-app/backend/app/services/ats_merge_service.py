import hashlib
import hmac
import json
import logging

from pydantic import validate_call

from app.core.config import settings
from app.modules.role.schemas import RoleATSSync
from app.services.exceptions import ExternalApiException

from .external_api_service import ExternalApiService

logger = logging.getLogger(__name__)


class ATSMergeService(ExternalApiService):
    base_url: str = settings.MERGE_TOOL_API_URL

    def _sign_request(self, body: dict, secret_key: str) -> str:
        message = json.dumps(body).encode("utf-8")
        secret = secret_key.encode("utf-8")

        signature = hmac.new(secret, message, digestmod=hashlib.sha256).digest()
        hex_encoded = signature.hex()

        return hex_encoded

    @validate_call(validate_return=True)
    def sync_role(self, ats_sync: RoleATSSync) -> str:
        signature = self._sign_request(ats_sync.model_dump(), settings.ECHO_API_SIGNATURE_KEY)

        res = self.post(
            endpoint="/candidates/jobs",
            json=ats_sync.model_dump(),
            headers={"X-Echo-Signature": signature},
        )

        if "job_id" not in res:
            raise ExternalApiException(detail=f"Job ID not found in response: {res}")

        return res["job_id"]
