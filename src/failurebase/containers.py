"""Containers module."""

from dependency_injector import containers, providers

from .adapters.database import Database
from .services.event import EventService
from .services.test import TestService
from .services.uow import DatabaseUnitOfWork
from .adapters.repositories.event import EventRepository
from .adapters.repositories.test import TestRepository


class Adapters(containers.DeclarativeContainer):
    """Container for adapters to database."""

    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.DATABASE_URI)

    event_repository = providers.Object(EventRepository)

    test_repository = providers.Object(TestRepository)


class Services(containers.DeclarativeContainer):
    """Container for all services."""

    config = providers.Configuration()

    adapters = providers.DependenciesContainer()

    database_unit_of_work = providers.Factory(
        DatabaseUnitOfWork,
        session_factory=adapters.db.provided.session_factory,
        event_repository_cls=adapters.event_repository,
        test_repository_cls=adapters.test_repository
    )

    event_service = providers.Factory(
        EventService,
        uow=database_unit_of_work,
    )

    test_service = providers.Factory(
        TestService,
        uow=database_unit_of_work,
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
