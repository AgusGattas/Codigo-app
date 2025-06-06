import json

from injector import Inject
from sqlalchemy import MetaData, create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from app.context import get_request_context, req_or_thread_id
from app.core.config import settings

meta = MetaData(
    naming_convention={
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }
)


class Base(DeclarativeBase):
    metadata = meta

    @classmethod
    def _display_name(self):
        return self.__tablename__.capitalize()


def create_sqlalchemy_engine(*, db_url: str, pool_size: int) -> Engine:
    return create_engine(
        db_url,
        pool_pre_ping=settings.DB_POOL_PRE_PING,
        pool_recycle=settings.POOL_RECYCLE_MINUTES * 60,
        echo=settings.DEBUG_MODE,
        pool_size=pool_size,
        max_overflow=100,
    )


class DatabaseResource:
    """Class to handle database connections and sessions"""

    def __init__(
        self,
        engine: Inject[Engine],
        admin_db_role: str = settings.DB_ADMIN_ROLE,
        auth_db_role: str = settings.DB_AUTH_ROLE,
    ):
        self.engine = engine
        self.admin_db_role = admin_db_role
        self.auth_db_role = auth_db_role

        self.session_factory = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine),
            scopefunc=req_or_thread_id,
        )
        self.session = self.session_factory

        self._add_session_event_listener()

    def _add_session_event_listener(self):
        """Attach a listener to run SQL when a session starts"""

        @event.listens_for(self.session_factory, "after_begin")
        def set_custom_config(session, transaction, connection):
            req_ctx = get_request_context()

            db_role = self.admin_db_role
            if settings.ENABLE_ACCESS_CONTROL and req_ctx.authenticated:
                db_role = self.auth_db_role

            custom_sql = text(
                """
                SELECT set_config(
                    'request.jwt.claims',
                    :jwt,
                    true
                );

                SET LOCAL statement_timeout=:timeout;

                SET LOCAL ROLE :role;
            """
            ).bindparams(
                jwt=json.dumps(req_ctx.jwt),
                role=db_role,
                timeout=settings.DB_STATEMENT_TIMEOUT_MS,
            )

            connection.execute(custom_sql)

    def create_database(self) -> None:
        Base.metadata.create_all(self.engine)

    def drop_database(self):
        Base.metadata.drop_all(self.engine)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if traceback:
            self.session.rollback()
        self.session.remove()


# Crear la instancia de engine y DatabaseResource
engine = create_sqlalchemy_engine(
    db_url=settings.DB_URL,
    pool_size=settings.DB_POOL_SIZE
)

db = DatabaseResource(engine=engine)
