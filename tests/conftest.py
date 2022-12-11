# flake8: noqa
import asyncio
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def event_loop(request: SubRequest):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture
# def event_loop():
#     """
#     Avoid receiving annoying warnings during tests execution
#     https://github.com/pytest-dev/pytest-asyncio/issues/371#issuecomment-1161462430
#     """
#
#     # https://github.com/pytest-dev/pytest-asyncio#event_loop
#
#     # https://docs.python.org/3.10/library/asyncio-policy.html#asyncio.get_event_loop_policy
#     # policy = asyncio.get_event_loop_policy()  # WindowsProactorEventLoopPolicy
#
#     # https://docs.python.org/3.10/library/asyncio-policy.html#asyncio.WindowsSelectorEventLoopPolicy
#     # TODO Should we use it also in Linux?
#     policy = asyncio.WindowsSelectorEventLoopPolicy()  # WindowsSelectorEventLoopPolicy
#
#     # https://docs.python.org/3.10/library/asyncio-policy.html#asyncio.AbstractEventLoopPolicy.new_event_loop
#     loop = policy.new_event_loop()  # WindowsSelectorEventLoop
#
#     # https://docs.python.org/3.10/library/asyncio-eventloop.html#asyncio.set_event_loop
#     asyncio.set_event_loop(loop)
#
#     yield loop
#
#     # You can skip the next call, it will be automatically called by pytest-asyncio plugin finalizer
#     # https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.hookspec.pytest_fixture_post_finalizer
#     # https://github.com/pytest-dev/pytest-asyncio/blob/d39589c0353657ee6d75d38db779cc4ecb2491c4/pytest_asyncio/plugin.py#L376
#     loop.close()


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(override=True)
