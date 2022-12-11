# PyCharm

https://plugins.jetbrains.com/plugin/14476-evaluate-async-code

# Links

- Azure SDK for Python https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview
- Azure libraries package index https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-library-package-index
- Organized by Azure service https://learn.microsoft.com/en-us/python/api/overview/azure/?view=azure-python
- Organized by package name https://learn.microsoft.com/en-us/python/api/?view=azure-python
- Code Samples of Azure Python SDK Management Libraries https://github.com/Azure-Samples/azure-samples-python-management
- Source code for the Azure libraries https://github.com/Azure/azure-sdk-for-python
- Authenticate Python apps to Azure services by using the Azure SDK for Python https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview
- Azure Identity client library for Python - version 1.11.0 https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python
- Methods returning collections (paging) https://azure.github.io/azure-sdk/python_design.html#methods-returning-collections-paging
- https://stackoverflow.com/a/65995209
  - https://docs.pytest.org/en/latest/how-to/logging.html#live-logs 
  - `--log-cli-level=INFO --capture=tee-sys`
- https://github.com/aio-libs/aioodbc 
  - Is run_in_executor optimized for running in a loop with coroutines? 
    - https://github.com/aio-libs/aioodbc/blob/master/aioodbc/connection.py#L78
    - https://stackoverflow.com/a/55030541
  - https://github.com/sqlalchemy/sqlalchemy/issues/6521#issuecomment-907387533
    - https://fastapi.tiangolo.com/async/#path-operation-functions
- When do I construct a Session, when do I commit it, and when do I close it?
  - https://docs.sqlalchemy.org/en/14/orm/session_basics.html#session-faq-whentocreate
- Using asyncio scoped session
  - https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-asyncio-scoped-session
- What is the proper way to type hint the return value of an @asynccontextmanager?
  - https://stackoverflow.com/questions/63125259/what-is-the-proper-way-to-type-hint-the-return-value-of-an-asynccontextmanager
- Using Thread-Local Scope with Web Applications
  - https://docs.sqlalchemy.org/en/14/orm/contextual.html#using-thread-local-scope-with-web-applications
- class dependency_injector.providers.ThreadLocalSingleton
  - https://python-dependency-injector.ets-labs.org/api/providers.html?highlight=thread#dependency_injector.providers.ThreadLocalSingleton
- Contextual/Thread-local Sessions
  - https://docs.sqlalchemy.org/en/14/orm/contextual.html
- Sub-dependencies
  - https://fastapi.tiangolo.com/async/#sub-dependencies
- Resources, wiring, and per-function execution scope
  - https://python-dependency-injector.ets-labs.org/providers/resource.html#resources-wiring-and-per-function-execution-scope
- FastAPI async resource not being closed
  - https://github.com/ets-labs/python-dependency-injector/issues/595#issuecomment-1225677845
- Async Tests
  - https://fastapi.tiangolo.com/advanced/async-tests/#httpx
- Calling into Python Web Apps
  - https://www.python-httpx.org/advanced/#calling-into-python-web-apps
- Use the app.dependency_overrides attribute
  - https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-appdependency_overrides-attribute

# Docker

`docker-compose -f C:\Temp\docker\postgres.yml up`