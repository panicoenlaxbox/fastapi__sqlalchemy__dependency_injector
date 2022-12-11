import pytest

from azure_sql.azure_sql_manager import AzureSqlManager

pytest.skip("Azure dependent", allow_module_level=True)


async def test_get_subscriptions():
    async with AzureSqlManager() as azure_sql_manager:
        async for subscription in azure_sql_manager.subscriptions.get_subscriptions():
            print(subscription)


async def test_get_servers():
    async with AzureSqlManager() as azure_sql_manager:
        async for subscription in azure_sql_manager.subscriptions.get_subscriptions():
            async for server in azure_sql_manager.get_servers(subscription.subscription_id):
                print(server)


async def test_get_databases():
    async with AzureSqlManager() as azure_sql_manager:
        async for subscription in azure_sql_manager.subscriptions.get_subscriptions():
            async for server in azure_sql_manager.get_servers(subscription.subscription_id):
                async for database in azure_sql_manager.get_databases(
                    subscription.subscription_id, server.resource_group_name, server.name
                ):
                    print(database)


async def test_get_database():
    async with AzureSqlManager() as azure_sql_manager:
        database = await azure_sql_manager.get_database(
            "a1f675b4-f74f-404e-8e2e-348a40cf7477",
            "rg-roivolution",
            "roivolution-db-server-pro",
            "RoivolutionARE000242",
        )
        print(database)


async def test_get_elastic_pools():
    async with AzureSqlManager() as azure_sql_manager:
        async for subscription in azure_sql_manager.subscriptions.get_subscriptions():
            async for server in azure_sql_manager.get_servers(subscription.subscription_id):
                async for elastic_pool in azure_sql_manager.get_elastic_pools(subscription.subscription_id, server):
                    print(elastic_pool)


async def test_get_elastic_pool():
    async with AzureSqlManager() as azure_sql_manager:
        elastic_pool = await azure_sql_manager.get_elastic_pool(
            "a1f675b4-f74f-404e-8e2e-348a40cf7477",
            "rg-roivolution",
            "roivolution-db-server-pro",
            "RoivolutionDbPoolPro",
            calculate_usage=True,
        )
        print(elastic_pool)
