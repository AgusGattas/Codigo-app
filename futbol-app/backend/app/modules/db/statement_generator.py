import logging
from typing import List, Type

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import (
    DeclarativeBase,
    InstrumentedAttribute,
    RelationshipProperty,
)

from app.modules.db.sqlalchemy import safe_getattr

from .ast import ASTNode, InheritedLoadNode, LoadOnlyNode, RelationshipLoadNode
from .code_generator import QueryOptionGenerator
from .pydantic_fields import PydanticGraph

logger = logging.getLogger(__name__)


class StatementGenerator:
    """Generates SQLAlchemy select statements based on Pydantic models."""

    def __init__(self, graph: PydanticGraph, model: Type[DeclarativeBase]):
        self.model = model
        self.graph = graph

    def generate_query(self):
        """Generate the SQLAlchemy select statement."""
        ast = self._build_ast()
        generator = QueryOptionGenerator()

        return [generator.visit(node) for node in ast.children if node]

    def _build_ast(self) -> ASTNode:
        return ASTNode(self.model, self._build_child_nodes(self.model, self.graph))

    def _build_relationship_nodes(
        self, model: Type[DeclarativeBase], graph: PydanticGraph
    ) -> List[ASTNode]:
        """Recursively build relationship nodes."""
        nodes: list[ASTNode] = []

        columns, relationships = self._categorize_columns(model, graph.relationships.keys())
        if columns:
            nodes.append(LoadOnlyNode(model, [], columns))

        for rel_node in relationships:
            sub_graph = graph.relationships[rel_node.relationship]
            rel_node.children = self._build_child_nodes(rel_node.mapper, sub_graph)

            nodes.append(rel_node)
        return nodes

    def _build_child_nodes(
        self, model: Type[DeclarativeBase], graph: PydanticGraph
    ) -> List[ASTNode]:
        columns, relationships = self._categorize_columns(model, graph.columns)

        children: list[ASTNode] = []
        if columns:
            children.append(LoadOnlyNode(model, [], columns))

        if relationships:
            children.extend(relationships)

        return children + self._build_relationship_nodes(model, graph)

    def _get_orm_relation(
        self, model: Type[DeclarativeBase], relationship_name: str
    ) -> Type[DeclarativeBase]:
        """Get the related model class for a relationship."""
        try:
            mapper = inspect(model)
            relationship_prop = mapper.relationships[relationship_name]
            return relationship_prop.mapper.class_
        except KeyError:
            raise AttributeError(
                f"Relationship `{relationship_name}` not found in model {model}"
            ) from None

    def _find_in_descendants(self, model: Type[DeclarativeBase], column: str):
        mapper = inspect(model)
        parent_table = mapper.local_table

        for subclass_mapper in mapper.self_and_descendants:
            if subclass_mapper.local_table != parent_table:
                if column in subclass_mapper.local_table.c:
                    return subclass_mapper.class_

    def _categorize_columns(
        self, model: Type[DeclarativeBase], columns: List[str]
    ) -> tuple[list[str], list[RelationshipLoadNode]]:
        """
        Categorize columns into relationships and scalars,
        skipping properties and non-sqlalchemy attributes.
        """
        relationships = []
        scalars = []

        for column in columns:
            attr = safe_getattr(model, column, default=None)

            if isinstance(attr, InstrumentedAttribute):
                if isinstance(attr.property, RelationshipProperty):
                    relationships.append(
                        RelationshipLoadNode(relationship=column, model=model, children=[])
                    )
                else:
                    scalars.append(column)
            else:
                # As a last attempt try to find it in inherited (children) tables
                descendant = self._find_in_descendants(model, column)
                if descendant:
                    relationships.append(
                        InheritedLoadNode(
                            relationship=column,
                            model=descendant,
                            children=[],
                        )
                    )
                else:
                    logger.debug(f"Skipping non-attribute {column} in model {model}")

        return scalars, relationships


def select_from_pydantic(model: Type[DeclarativeBase], schema: BaseModel):
    graph = PydanticGraph.from_model(schema)
    generator = StatementGenerator(graph, model)
    return generator.generate_query()
