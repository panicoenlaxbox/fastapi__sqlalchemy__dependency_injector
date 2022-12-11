import uuid
from http import HTTPStatus

from assertpy import assert_that
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from azure_sql import models, schemas
from azure_sql.containers import Container


async def test_get_subscription(session: AsyncSession, http_client: AsyncClient):
    await session.execute(delete(models.Subscription))
    db_subscription = models.Subscription(
        subscription_id=uuid.UUID("0fdff486-1af4-412b-8933-7a5c7884729f"), display_name="Subscription_1", enabled=True
    )
    session.add(db_subscription)

    response = await http_client.get(f"/subscriptions/{db_subscription.subscription_id}")

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    assert_that(schemas.Subscription(**response.json())).is_equal_to(
        schemas.Subscription(
            subscription_id=db_subscription.subscription_id,
            display_name=db_subscription.display_name,
            enabled=db_subscription.enabled,
        )
    )


async def test_get_subscriptions(session_provider, container: Container, http_client: AsyncClient):
    async with session_provider() as session:
        await session.execute(delete(models.Subscription))
        db_subscription = models.Subscription(
            subscription_id=uuid.UUID("0fdff486-1af4-412b-8933-7a5c7884729f"),
            display_name="Subscription_1",
            enabled=True,
        )
        session.add(db_subscription)

        with container.session_provider.override(session_provider):
            response = await http_client.get("/subscriptions/")

    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    json = response.json()
    assert_that(schemas.Subscription(**json[0])).is_equal_to(
        schemas.Subscription(
            subscription_id=db_subscription.subscription_id,
            display_name=db_subscription.display_name,
            enabled=db_subscription.enabled,
        )
    )
