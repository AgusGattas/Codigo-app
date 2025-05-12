from typing import Iterable, List, Optional, Type

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class ASTNode:
    """Base class for all AST nodes."""

    def __init__(self, model: type[DeclarativeBase], children: Optional[List["ASTNode"]]):
        self.model = model
        self.children = children or []

    def visualize(self, indent: int = 0):
        indentation = "\t" * indent
        kwargs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())

        print(f"{indentation}{self.__class__.__name__}({kwargs})")

        for child in self.children:
            child.visualize(indent + 1)

    def __eq__(self, other: object) -> bool:
        return self.__dict__ == other.__dict__


class LoadOnlyNode(ASTNode):
    """Represents a load_only operation on a model with specified columns."""

    def __init__(
        self,
        model: type[DeclarativeBase],
        children: Optional[List["ASTNode"]],
        columns: Iterable[str],
    ):
        self.columns = columns

        super().__init__(model, children)


class RelationshipLoadNode(ASTNode):
    """Represents a relationship loading operation."""

    def __init__(
        self,
        model: type[DeclarativeBase],
        children: Optional[List[ASTNode]],
        relationship: str,
    ):
        self.relationship = relationship
        super().__init__(model, children)

    @property
    def mapper(self) -> Type[DeclarativeBase]:
        """Get the related model class for a relationship."""
        try:
            mapper = inspect(self.model)
            relationship_prop = mapper.relationships[self.relationship]
            return relationship_prop.mapper.class_
        except KeyError:
            raise AttributeError(
                f"Relationship `{self.relationship}` not found in model {self.model}"
            ) from None


class InheritedLoadNode(RelationshipLoadNode):
    """Represents a load operation on an inherited model."""

    @property
    def mapper(self) -> Type[DeclarativeBase]:
        """Get the related model class for a relationship."""
        return self.model
