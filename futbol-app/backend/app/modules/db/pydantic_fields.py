from collections import deque
from typing import Any, Iterator, Optional, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo

SELECT_STRATEGY_KEY = "_select_strategy"


def pydantic_field_name(name: str, field: FieldInfo):
    if field.alias:
        return field.alias

    if field.validation_alias:
        if isinstance(field.validation_alias, str):
            return field.validation_alias

        return ".".join(field.validation_alias.path)

    return name


def should_ignore_field(field: FieldInfo) -> bool:
    if field.json_schema_extra:
        return field.json_schema_extra.get(SELECT_STRATEGY_KEY) == "lazy"
    return False


# TODO: We're not dealing with Recursive models
def pydantic_model_fields(model: type[BaseModel], prefix="") -> Iterator[str]:
    """
    Returns flat names for all fields in a Pydantic model.
    """

    def _pydantic_model(ann: Any) -> Optional[type[BaseModel]]:
        if get_origin(ann):
            # NOTE: we're checking **every** type that's not a atomic: dict/list/union/generic etc.
            # NOTE: update this so we only check the types we're interested in Union/list/set/tuple.
            for arg in get_args(ann):
                if pydantic_model := _pydantic_model(arg):
                    return pydantic_model

        if isinstance(ann, type) and issubclass(ann, BaseModel):
            return ann

        return None

    queue = deque([(prefix, model)])

    while queue:
        prefix, model = queue.popleft()
        for name, field in model.model_fields.items():
            if should_ignore_field(field):
                continue

            ann = field.annotation
            field_name = pydantic_field_name(name, field)

            if pydantic_model := _pydantic_model(ann):
                queue.append(
                    (f"{prefix}{field_name}.", pydantic_model),
                )
            else:
                yield f"{prefix}{field_name}"


class PydanticGraph:
    """
    Graph that represents the field structure and relationships
    of a Pydantic model.
    """

    def __init__(self, columns: list[str], relationships: dict[str, "PydanticGraph"]):
        self.columns: list[str] = columns
        self.relationships: dict[str, "PydanticGraph"] = relationships

    def add_node(self, node: str):
        if "." in node:
            relationship, sub_node = node.split(".", 1)

            if relationship not in self.relationships:
                self.relationships[relationship] = PydanticGraph([], {})
            self.relationships[relationship].add_node(sub_node)
        else:
            self.columns.append(node)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PydanticGraph):
            return False

        return self.columns == other.columns and self.relationships == other.relationships

    @classmethod
    def from_model(cls, fields: type[BaseModel]) -> "PydanticGraph":
        model_fields = pydantic_model_fields(fields)

        graph = cls([], {})
        for field in model_fields:
            graph.add_node(field)
        return graph
