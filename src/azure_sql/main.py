import uvicorn

from azure_sql.application import create_app
from azure_sql.database import engine

app = create_app()


@app.get("/")
async def root():
    return "Hello World!"


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
