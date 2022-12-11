import threading
import uuid
from random import randrange

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from azure_sql import models
from azure_sql.dependencies import get_session

ROUTER_NAME = "debug"
router = APIRouter(prefix=f"/{ROUTER_NAME}", tags=[ROUTER_NAME])


@router.get("/")
@inject
async def get_debug(session: AsyncSession = Depends(get_session)):
    db_subscription = models.Subscription(
        subscription_id=uuid.uuid4(), display_name=f"Subscription_{randrange(100)}", enabled=True
    )
    session.add(db_subscription)
    return {"session_id": id(session), "session_new": session.new, "thread_id": threading.get_ident()}
