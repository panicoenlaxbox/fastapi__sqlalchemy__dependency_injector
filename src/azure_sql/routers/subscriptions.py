from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from mediatpy import Mediator
from sqlalchemy.ext.asyncio import AsyncSession

from azure_sql import models, schemas
from azure_sql.containers import Container
from azure_sql.dependencies import get_session
from azure_sql.handlers import GetSubscriptionsRequest

ROUTER_NAME = "subscriptions"
router = APIRouter(prefix=f"/{ROUTER_NAME}", tags=[ROUTER_NAME])


@router.get("/", response_model=list[schemas.Subscription])
@inject
async def get_subscriptions(mediator: Mediator = Depends(Provide[Container.mediator])):
    return await mediator.send(GetSubscriptionsRequest())


@router.get("/{subscription_id}", response_model=schemas.Subscription)
@inject
async def get_subscription(subscription_id: UUID, session: AsyncSession = Depends(get_session)):
    return await session.get(models.Subscription, subscription_id)
