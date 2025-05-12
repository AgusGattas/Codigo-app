from sqlalchemy.orm import DeclarativeBase


class SentinelDefaultValue:
    ...


def safe_getattr(obj: type[DeclarativeBase], attr: str, *, default=SentinelDefaultValue):
    try:
        return getattr(obj, attr)
    except AttributeError as e:
        if default is not SentinelDefaultValue:
            return default

        raise AttributeError(
            f"Column/Relationship `{attr}` not found in model {obj.__name__}: {e}"
        ) from e
