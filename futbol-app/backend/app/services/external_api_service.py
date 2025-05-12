import requests
from loguru import logger
from pydantic import BaseModel, ConfigDict

from app.services.exceptions import ExternalApiException


class ExternalApiService(BaseModel):
    headers: dict = {}
    base_url: str
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    return_json: bool = True

    def __hash__(self) -> int:
        return hash(self.base_url)

    def post(self, endpoint, **kwargs):
        return self.__send_request(endpoint, method="post", **kwargs)

    def get(self, endpoint, **kwargs):
        return self.__send_request(endpoint, method="get", **kwargs)

    def put(self, endpoint, **kwargs):
        return self.__send_request(endpoint, method="put", **kwargs)

    def patch(self, endpoint, **kwargs):
        return self.__send_request(endpoint, method="patch", **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.__send_request(endpoint, method="delete", **kwargs)

    def _error_message(self, response):
        try:
            err = response.json()

            details = err.get("detail", [])
            if isinstance(details, str):
                details = [{"msg": details}]

            for detail in details:
                detail["source"] = "external"

            return details or err
        except (ValueError, TypeError):
            return response.text

    def __send_request(self, endpoint: str, method: str, headers: dict = None, **kwargs):
        url = self.base_url + endpoint
        headers = headers or self.headers

        # Log request details
        logger.info(f"Sending {method.upper()} request to {url}")
        if kwargs.get("json"):
            logger.debug(f"Request body: {kwargs['json']}")
        elif kwargs.get("data"):
            logger.debug(f"Request data: {kwargs['data']}")

        try:
            response = requests.request(
                method=method, url=url, headers=headers, **kwargs, timeout=300
            )

            # Log response details
            logger.info(f"Received response from {url} - Status: {response.status_code}")
            if response.status_code == 200:
                if self.return_json:
                    logger.debug(f"Response body: {response.json()}")

            response.raise_for_status()
            if self.return_json:
                return response.json()
            return response

        except requests.exceptions.HTTPError as err:
            error_details = self._error_message(response)
            logger.error(
                f"HTTP Error calling {url}\n"
                f"Status Code: {response.status_code}\n"
                f"Method: {method.upper()}\n"
                f"Error Details: {error_details}"
            )
            raise ExternalApiException(
                status_code=response.status_code, detail=error_details
            ) from err
        except requests.exceptions.RequestException as err:
            logger.error(
                f"Request failed for {url}\n" f"Method: {method.upper()}\n" f"Error: {str(err)}"
            )
            raise ExternalApiException(
                status_code=500,
                detail=[{"msg": f"Request failed: {str(err)}", "source": "external"}],
            ) from err
