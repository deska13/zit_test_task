import logging
import re
from types import TracebackType
from typing import Self, Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .product import ProductRepositry
from .product_type import ProductTypeRepositry

logger = logging.getLogger(__name__)

ALLOWED_EXCEPTIONS = ()
id_key_exists_pattern = re.compile(
    r"KEY \(id\)=[^\(]*(\(.*\))[^\)]*already exists", re.IGNORECASE
)


def check_id_already_exists(error: IntegrityError) -> bool:
    pattern = id_key_exists_pattern
    return bool(pattern.search(str(error.orig)))


class SQLAlchemyUnitOfWork:
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._is_event_collected = False
        super().__init__()

    async def __aenter__(self) -> Self:
        self._is_event_collected = False
        self.session = self._session_factory()
        if self.session:
            self.product = ProductRepositry(self.session)
            self.product_type = ProductTypeRepositry(self.session)

        return self

    async def __aexit__(
        self,
        exc_type: Type[Exception] | None,
        exc: Exception | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None and exc_type not in ALLOWED_EXCEPTIONS:
            exc_info: bool | tuple[type[Exception], Exception, TracebackType] = True
            if exc_type is not None and exc is not None and traceback is not None:
                exc_info = (exc_type, exc, traceback)
            logger.error("An error occurred during transaction", exc_info=exc_info)
        await self.rollback()
        if self.session is not None:
            await self.session.close()
        self.session = None

    async def rollback(self) -> None:
        if self.session is not None:
            await self.session.rollback()
