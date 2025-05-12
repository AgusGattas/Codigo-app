from typing import Callable

from sqlalchemy import Insert

OnConflictClause = Callable[[Insert], Insert]


def do_nothing_on_conflict(insert: Insert, **kwargs) -> Insert:
    return insert.on_conflict_do_nothing(**kwargs)


def do_update_on_conflict(insert: Insert, **kwargs) -> Insert:
    return insert.on_conflict_do_update(**kwargs)


def do_default_on_conflict(insert: Insert) -> Insert:
    return insert
