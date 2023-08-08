"""Containers module."""

from dependency_injector import containers, providers

from failurebase.adapters.database import Database
from failurebase.adapters.repositories.event import EventRepository
from failurebase.adapters.repositories.test import TestRepository
from failurebase.adapters.repositories.client import ClientRepository
from failurebase.adapters.repositories.api_key import ApiKeyRepository
from failurebase.services.event.service import EventService
from failurebase.services.test.service import TestService
from failurebase.services.client.service import ClientService
from failurebase.services.api_key.service import ApiKeyService
from failurebase.services.event.uow import EventUnitOfWork
from failurebase.services.test.uow import TestUnitOfWork
from failurebase.services.client.uow import ClientUnitOfWork
from failurebase.services.api_key.uow import ApiKeyUnitOfWork
from failurebase.managers.token import JwtTokenManager
from failurebase.managers.secret import SecretManager


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

    event_unit_of_work = providers.Factory(
        EventUnitOfWork,
        session_factory=adapters.db.provided.session_factory,
        event_repository_cls=adapters.event_repository,
        test_repository_cls=adapters.test_repository,
        client_repository_cls=adapters.client_repository,
    )

    test_unit_of_work = providers.Factory(
        TestUnitOfWork,
        session_factory=adapters.db.provided.session_factory,
        test_repository_cls=adapters.test_repository
    )

    client_unit_of_work = providers.Factory(
        ClientUnitOfWork,
        session_factory=adapters.db.provided.session_factory,
        client_repository_cls=adapters.client_repository,
    )

    api_key_unit_of_work = providers.Factory(
        ApiKeyUnitOfWork,
        session_factory=adapters.db.provided.session_factory,
        api_key_repository_cls=adapters.api_key_repository,
    )

    event_service = providers.Factory(
        EventService,
        uow=event_unit_of_work,
    )

    test_service = providers.Factory(
        TestService,
        uow=test_unit_of_work,
    )

    client_service = providers.Factory(
        ClientService,
        uow=client_unit_of_work,
    )

    api_key_service = providers.Factory(
        ApiKeyService,
        uow=api_key_unit_of_work,
    )


class Managers(containers.DeclarativeContainer):
    """Container for all managers."""

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
