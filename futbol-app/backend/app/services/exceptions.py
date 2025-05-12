from app.exceptions import HTTPExceptionMixin


class ExternalApiException(HTTPExceptionMixin):
    """Base external API exception"""

    detail = "External API error"
    error_code = "external_api_error"
    status_code = 500


class AlreadyDeletedUserException(HTTPExceptionMixin):
    """User already deleted exception"""

    detail = "User already deleted"
    error_code = "user_already_deleted"
    status_code = 400
