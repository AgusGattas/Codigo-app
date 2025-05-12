from typing import Any, Optional, Type

from fastapi_pagination import Params, create_page
from fastapi_pagination.api import apply_items_transformer
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.ext.sqlalchemy import (
    SyncConn,
    UnwrapMode,
    _maybe_unique,
    _unwrap_items,
)
from fastapi_pagination.types import AdditionalData, ItemsTransformer
from sqlalchemy import Selectable
from sqlalchemy.orm import Session

from app.database.base import Base


def execute_cte_pagination(
    query: Selectable,
    count_query: Optional[Selectable],
    params: AbstractParams,
    conn: SyncConn,
    transformer: Optional[ItemsTransformer] = None,
    additional_data: Optional[AdditionalData] = None,
    unique: bool = True,
    unwrap_mode: Optional[UnwrapMode] = None,
) -> AbstractPage[Any]:
    items = _maybe_unique(conn.execute(query), unique)
    items = _unwrap_items(items, query, unwrap_mode)
    items = apply_items_transformer(items, transformer)

    return create_page(
        items,
        total=conn.scalar(count_query),
        params=params,
        **(additional_data or {}),
    )


def cte_pagination(
    model: Type[Base],
    session: Session,
    query: Selectable,
    pre_filter_query: Selectable,
    count_query: Selectable,
    pagination_params: Params,
    **kwargs,
) -> AbstractPage[Any]:
    """
    Paginate a query using a CTE pre-filter.

    Args:
        session (Session): The SQLAlchemy session.
        query (Selectable): The main query to get the items.
        pre_filter_query (Selectable): The query to get the ids of the items to be paginated.
        count_query (Selectable): The query to count the total number of items.
        pagination_params (Params): The pagination parameters.

    Returns:
        AbstractPage[Any]: The paginated items.
    """
    raw_params = pagination_params.to_raw_params().as_limit_offset()
    pre_filter_query = pre_filter_query.limit(raw_params.limit).offset(raw_params.offset)
    cte_query = pre_filter_query.cte("__pre_filter_ids_cte")

    response_query = query.join(cte_query, model.id == cte_query.c.id)
    return execute_cte_pagination(
        conn=session,
        query=response_query,
        count_query=count_query,
        params=pagination_params,
        **kwargs,
    )
