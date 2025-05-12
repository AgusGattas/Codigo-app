from sqlalchemy import exc
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import joinedload, load_only

from app.modules.db.sqlalchemy import safe_getattr

from .ast import ASTNode, InheritedLoadNode, LoadOnlyNode, RelationshipLoadNode


class QueryOptionGenerator:
    """Visitor class that generates SQLAlchemy query options from AST nodes."""

    def visit(self, node: ASTNode):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode):
        """Fallback method if no visit method is found for a node."""
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_LoadOnlyNode(self, node: LoadOnlyNode):
        orm_columns = (safe_getattr(node.model, col) for col in node.columns)

        try:
            return load_only(*orm_columns)
        except exc.ArgumentError as e:
            return self._argument_error(e, node)

    def visit_RelationshipLoadNode(self, node: RelationshipLoadNode):
        relationship = safe_getattr(node.model, node.relationship)

        loader = joinedload(relationship)
        if node.children:
            child_loaders = [self.visit(child) for child in node.children]
            loader = loader.options(*child_loaders)

        return loader

    def visit_InheritedLoadNode(self, node: InheritedLoadNode):
        return load_only(safe_getattr(node.model, node.relationship))

    def _argument_error(self, e: exc.ArgumentError, node: LoadOnlyNode):
        """
        Sometimes we get an "ArgumentError" from sqlalchemy because we added a non-column field
        into the select statement.

        Here we will try to figure out which field is causing the issue and raise a more
        informative error message.
        """

        for col in node.columns:
            orm_column = safe_getattr(node.model, col)

            try:
                inspect(orm_column)
            except exc.NoInspectionAvailable:
                raise AttributeError(
                    f"Column `{col}` in model {node.model.__name__} is not a column field"
                ) from e

        raise e
