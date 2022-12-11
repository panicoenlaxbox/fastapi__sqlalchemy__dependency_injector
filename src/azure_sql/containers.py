from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from azure_sql.database import session_provider


def _noop():
    return providers.Singleton(lambda *args, **kwargs: None)


class Container(DeclarativeContainer):
    # https://python-dependency-injector.ets-labs.org/api/providers.html?highlight=thread#dependency_injector.providers.ThreadLocalSingleton
    # https://docs.sqlalchemy.org/en/14/orm/contextual.html
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-asyncio-scoped-session
    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    # https://fastapi.tiangolo.com/async/#sub-dependencies
    # https://python-dependency-injector.ets-labs.org/providers/resource.html#resources-wiring-and-per-function-execution-scope
    # https://github.com/ets-labs/python-dependency-injector/issues/595#issuecomment-1225677845
    session_provider = providers.Object(session_provider)

    mediator = _noop()
