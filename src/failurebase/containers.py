"""Containers module."""

from dependency_injector import containers, providers

from .adapters.database import Database
from .services.event import EventService
from .services.test import TestService
from .services.client import ClientService
from .services.uow import DatabaseUnitOfWork
from .services.api_key import ApiKeyService
from .managers.token import JwtTokenManager
from .managers.secret import SecretManager
from .adapters.repositories.event import EventRepository
from .adapters.repositories.test import TestRepository
from .adapters.repositories.client import ClientRepository
from .adapters.repositories.api_key import ApiKeyRepository


class Adapters(containers.DeclarativeContainer):
    """Container for adapters to database."""

    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.DATABASE_URI)

    event_repository = providers.Object(EventRepository)

    test_repository = providers.Object(TestRepository)

    client_repository = providers.Object(ClientRepository)

    api_key_repository = providers.Object(ApiKeyRepository)


class Services(containers.DeclarativeContainer):
    """Container for all services."""

    config = providers.Configuration()

    adapters = providers.DependenciesContainer()

    database_unit_of_work = providers.Factory(
        DatabaseUnitOfWork,
        session_factory=adapters.db.provided.session_factory,
        event_repository_cls=adapters.event_repository,
        test_repository_cls=adapters.test_repository,
        client_repository_cls=adapters.client_repository,
        api_key_repository_cls=adapters.api_key_repository
    )

    event_service = providers.Factory(
        EventService,
        uow=database_unit_of_work,
    )

    test_service = providers.Factory(
        TestService,
        uow=database_unit_of_work,
    )

    client_service = providers.Factory(
        ClientService,
        uow=database_unit_of_work,
    )

    api_key_service = providers.Factory(
        ApiKeyService,
        uow=database_unit_of_work,
    )


class Managers(containers.DeclarativeContainer):
    """Container for all services."""

    config = providers.Configuration()

    secret_manager = providers.Factory(
        SecretManager,
        secret_key=config.SECRET_KEY
    )

    jwt_manager = providers.Factory(
        JwtTokenManager,
        secret_key=config.SECRET_KEY
    )


class Application(containers.DeclarativeContainer):
    """Main container."""
    
    wiring_config = containers.WiringConfiguration(packages=['.endpoints'])

    config = providers.Configuration()

    adapters = providers.Container(
        Adapters,
        config=config,
    )

    services = providers.Container(
        Services,
        config=config,
        adapters=adapters,
    )

    managers = providers.Container(
        Managers,
        config=config
    )
