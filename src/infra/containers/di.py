from dishka import BaseScope, Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infra.settings import PostgresSettings
from repository import SQLAlchemyUnitOfWork
from services import ProductService, ProductTypeService


class DiProvider(Provider):
    def __init__(self, scope: BaseScope | None = None, component: str | None = None):
        super().__init__(scope, component)

        self.postgres_settings = PostgresSettings()

    @provide(scope=Scope.APP)
    def get_sqlalchemy_engine(self) -> AsyncEngine:
        return create_async_engine(self.postgres_settings.dsn.unicode_string())

    @provide(scope=Scope.APP)
    async def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide(scope=Scope.APP)
    def get_repository_uow(
        self,
        sessionmaker: async_sessionmaker,
    ) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(sessionmaker)

    @provide(scope=Scope.APP)
    async def get_product_service(
        self, repository_uow: SQLAlchemyUnitOfWork
    ) -> ProductService:
        return ProductService(repository_uow)

    @provide(scope=Scope.APP)
    def get_product_type_service(
        self,
        repository_uow: SQLAlchemyUnitOfWork,
    ) -> ProductTypeService:
        return ProductTypeService(repository_uow)
