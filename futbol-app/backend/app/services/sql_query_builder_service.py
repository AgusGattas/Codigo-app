from typing import Annotated

from pydantic import AfterValidator, BaseModel, validate_call

from app.core.config import settings

from .external_api_service import ExternalApiService

CompanySQLQuery = Annotated[
    str,
    AfterValidator(lambda v: v.strip().replace(";", "")),
]


class SearchSQLResponse(BaseModel):
    sql_query: CompanySQLQuery


class SQLQueryBuilderService(ExternalApiService):
    base_url: str = settings.SQL_QUERY_BUILDER_API_URL
    headers: dict = {
        "X-Echo-internal": settings.ECHO_INTERNAL_API_KEY,
    }

    @validate_call(validate_return=True)
    def get_companies_sql_query(self, search_text: str) -> SearchSQLResponse:
        """
        Get a SQL query to search for companies by the given criteria.

        Args:
            search_text (str): Natural language description of what to search for

        Returns:
            SearchSQLResponse: A SQL query that will be used to search for companies by the given criteria. Using the defined VIEW in the database.
        """

        return self.post(endpoint="/companies/search", json={"search_text": search_text})
