import logging

from app.core.config import settings

from .external_api_service import ExternalApiService

logger = logging.getLogger(__name__)


class GrammarCheckerService(ExternalApiService):
    base_url: str = settings.GRAMMAR_CHECKER_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    def spell_check(self, text: str):
        if not text:
            return text

        data = {
            "resume": text,
        }

        try:
            res = self.post(endpoint="/grammar_checker/resume", json=data)
            out = res["checked_text"]

            return out
        except Exception as e:
            logger.exception("Grammar checker service failed")
            logger.exception(e)

            # If the service fails, return the original text
            return text
