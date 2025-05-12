"""Module with the Base service"""

import uuid
from typing import List

from fastapi_filter.base.filter import BaseFilterModel
from fastapi_pagination import Page, Params
from pydantic import BaseModel

from app.repositories.base_repository import BaseRepository, T


class BaseService:
    """Service to interact with entity collection.

    Args:
        db (DatabaseResource): DB instance for handling SQL queries
    """

    def __init__(self, repo: BaseRepository) -> None:
        self.repo = repo

    def get_by_id(
        self, entity_id: uuid.UUID, raise_error: bool = True, response_model: BaseModel = None
    ) -> T | None:
        return self.repo.get(entity_id, raise_error=raise_error, response_model=response_model)

    def get_all(
        self,
        entity_filter: BaseFilterModel | None = None,
        pagination_params: Params | None = None,
        **kwargs,
    ) -> List[T] | Page[T]:
        return self.repo.get_all(entity_filter, pagination_params, **kwargs)

    def create(self, entity: BaseModel, **extra_fields) -> T:
        return self.repo.save(entity, **extra_fields)

    def update(self, entity_id: uuid.UUID, entity: BaseModel) -> T:
        return self.repo.update(entity_id, entity)

    def delete(self, entity_id: uuid.UUID) -> None:
        return self.repo.delete(entity_id)
