import re
from dataclasses import dataclass
from typing import AsyncIterator, cast

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.sql.aio import SqlManagementClient
from azure.mgmt.sql.models import Database, DatabaseUsage, ElasticPool, Server
from azure.mgmt.subscription.aio import SubscriptionClient
from azure.mgmt.subscription.models import Subscription, SubscriptionState


@dataclass
class AzureSubscription:
    subscription_id: str
    display_name: str
    enabled: bool


@dataclass
class AzureSqlServer:
    resource_group_name: str
    name: str
    fully_qualified_domain_name: str
    state: str


@dataclass
class Size:
    bytes: float

    @property
    def kilobytes(self) -> float:
        return self.bytes / 1024

    @property
    def megabytes(self) -> float:
        return self.kilobytes / 1024

    @property
    def gigabytes(self) -> float:
        return self.megabytes / 1024

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bytes=},{self.kilobytes=},{self.megabytes=},{self.gigabytes=})"


@dataclass
class AzureSqlDatabaseUsage:
    space_used: Size
    space_allocated: Size
    space_allocated_unused: Size


@dataclass
class AzureSqlElasticPool:
    resource_group_name: str
    name: str
    server_name: str
    max_size: Size
    usage: AzureSqlDatabaseUsage | None = None


@dataclass
class AzureSqlDatabase:
    resource_group_name: str
    server_name: str
    name: str
    status: str
    current_service_objective_name: str
    max_size: Size
    usage: AzureSqlDatabaseUsage
    elastic_pool_name: str | None = None

    @property
    def is_elastic_pool(self):
        return self.elastic_pool_name is not None


class AzureSqlManager:
    def __init__(self):
        self._credential = DefaultAzureCredential()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._credential.close()

    @staticmethod
    def _get_resource_group_name_from_id(id_: str) -> str:
        match = re.search(r"resourceGroups\/(.+?)\/", id_)
        if match is None:
            raise ValueError("resource group not found.")
        return match.group(1)

    @staticmethod
    def _get_elastic_pool_name_from_id(elastic_pool_id: str) -> str | None:
        if elastic_pool_id is None:
            return None
        return str(elastic_pool_id.split("/")[-1])

    @staticmethod
    async def _get_database_usage(
        sql_client: SqlManagementClient, resource_group_name: str, server_name: str, database_name: str
    ) -> AzureSqlDatabaseUsage:
        space_used = 0.0
        space_allocated = 0.0
        database_usage: DatabaseUsage
        async for database_usage in sql_client.database_usages.list_by_database(
            resource_group_name, server_name, database_name
        ):
            if database_usage.name == "database_size":
                space_used = database_usage.current_value
            elif database_usage.name == "database_allocated_size":
                space_allocated = database_usage.current_value
        space_allocated_unused = space_allocated - space_used
        return AzureSqlDatabaseUsage(Size(space_used), Size(space_allocated), Size(space_allocated_unused))

    @staticmethod
    def _create_subscription(subscription: Subscription) -> AzureSubscription:
        state = cast(SubscriptionState, subscription.state)
        return AzureSubscription(
            cast(str, subscription.subscription_id),
            cast(str, subscription.display_name),
            state == SubscriptionState.ENABLED,
        )

    @classmethod
    def _create_database(
        cls, resource_group_name: str, server_name: str, database: Database, usage: AzureSqlDatabaseUsage
    ) -> AzureSqlDatabase:
        return AzureSqlDatabase(
            resource_group_name,
            server_name,
            database.name,
            database.status,
            database.current_service_objective_name,
            Size(database.max_size_bytes),
            usage,
            cls._get_elastic_pool_name_from_id(database.elastic_pool_id),
        )

    def _create_server(self, server: Server) -> AzureSqlServer:
        return AzureSqlServer(
            self._get_resource_group_name_from_id(server.id),
            server.name,
            server.fully_qualified_domain_name,
            server.state,
        )

    async def get_subscription(self, subscription_id: str) -> AzureSubscription:
        async with SubscriptionClient(self._credential) as client:
            subscription = await client.subscriptions.get(subscription_id)
            return self._create_subscription(subscription)

    async def get_subscriptions(self) -> AsyncIterator[AzureSubscription]:
        async with SubscriptionClient(self._credential) as client:
            subscription: Subscription
            async for subscription in client.subscriptions.list():
                yield self._create_subscription(subscription)

    async def get_server(self, subscription_id: str, resource_group_name: str, server_name: str) -> AzureSqlServer:
        async with SqlManagementClient(self._credential, subscription_id) as sql_client:
            server = await sql_client.servers.get(resource_group_name, server_name)
            return self._create_server(server)

    async def get_servers(self, subscription_id: str) -> AsyncIterator[AzureSqlServer]:
        async with SqlManagementClient(self._credential, subscription_id) as sql_client:
            server: Server
            async for server in sql_client.servers.list():
                yield self._create_server(server)

    async def get_databases(
        self, subscription_id: str, resource_group_name: str, server_name: str
    ) -> AsyncIterator[AzureSqlDatabase]:
        async with SqlManagementClient(self._credential, subscription_id) as sql_client:
            database: Database
            async for database in sql_client.databases.list_by_server(resource_group_name, server_name):
                if database.name == "master":
                    continue
                usage = await self._get_database_usage(sql_client, resource_group_name, server_name, database.name)
                yield self._create_database(
                    resource_group_name,
                    server_name,
                    database,
                    usage,
                )

    async def get_database(
        self, subscription_id: str, resource_group_name: str, server_name: str, database_name: str
    ) -> AzureSqlDatabase:
        async with SqlManagementClient(self._credential, subscription_id) as sql_client:
            database = await sql_client.databases.get(resource_group_name, server_name, database_name)
            usage = await self._get_database_usage(sql_client, resource_group_name, server_name, database.name)
            return self._create_database(resource_group_name, server_name, database, usage)

    async def _calculate_elastic_pool_database_usage(
        self, sql_client: SqlManagementClient, resource_group_name: str, server_name: str, elastic_pool_name: str
    ) -> AzureSqlDatabaseUsage:
        usages: list[AzureSqlDatabaseUsage] = []
        async for database in sql_client.databases.list_by_elastic_pool(
            resource_group_name, server_name, elastic_pool_name
        ):
            usages.append(await self._get_database_usage(sql_client, resource_group_name, server_name, database.name))
        return AzureSqlDatabaseUsage(
            Size(sum([usage.space_used.bytes for usage in usages])),
            Size(sum([usage.space_allocated.bytes for usage in usages])),
            Size(sum([usage.space_allocated_unused.bytes for usage in usages])),
        )

    async def _create_elastic_pool(
        self,
        sql_client: SqlManagementClient,
        resource_group_name: str,
        server_name: str,
        elastic_pool: ElasticPool,
        calculate_usage: bool,
    ) -> AzureSqlElasticPool:
        return AzureSqlElasticPool(
            resource_group_name,
            elastic_pool.name,
            server_name,
            Size(elastic_pool.max_size_bytes),
            await self._calculate_elastic_pool_database_usage(
                sql_client, resource_group_name, server_name, elastic_pool.name
            )
            if calculate_usage
            else None,
        )

    async def get_elastic_pools(
        self, subscription_id: str, resource_group_name: str, server_name: str, calculate_usage=False
    ) -> AsyncIterator[AzureSqlElasticPool]:
        async with SqlManagementClient(self._credential, subscription_id) as sql_client:
            elastic_pool: ElasticPool
            async for elastic_pool in sql_client.elastic_pools.list_by_server(resource_group_name, server_name):
                yield await self._create_elastic_pool(
                    sql_client, resource_group_name, server_name, elastic_pool, calculate_usage
                )

    async def get_elastic_pool(
        self,
        subscription_id: str,
        resource_group_name: str,
        server_name: str,
        elastic_pool_name: str,
        calculate_usage=False,
    ) -> AzureSqlElasticPool:
        async with SqlManagementClient(self._credential, subscription_id) as sql_client:
            elastic_pool = await sql_client.elastic_pools.get(resource_group_name, server_name, elastic_pool_name)
            return await self._create_elastic_pool(
                sql_client, resource_group_name, server_name, elastic_pool, calculate_usage
            )
