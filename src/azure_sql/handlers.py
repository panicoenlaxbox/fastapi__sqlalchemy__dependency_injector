from dependency_injector.wiring import Provide, inject
from mediatpy import Mediator, Request, RequestHandler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from azure_sql import models, schemas
from azure_sql.containers import Container

mediator = Mediator()


class GetSubscriptionsRequest(Request[list[schemas.Subscription]]):
    pass


@mediator.request_handler
@inject
class GetSubscriptionsRequestHandler(RequestHandler[GetSubscriptionsRequest, list[schemas.Subscription]]):
    def __init__(self, session_provider=Provide[Container.session_provider]) -> None:
        self._session_provider = session_provider

    async def handle(self, request: GetSubscriptionsRequest) -> list[schemas.Subscription]:
        session: AsyncSession
        async with self._session_provider() as session:
            subscriptions: list[models.Subscription] = (
                (await session.execute(select(models.Subscription))).scalars().all()
            )
            return [schemas.Subscription.from_orm(subscription) for subscription in subscriptions]
