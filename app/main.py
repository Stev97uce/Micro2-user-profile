from fastapi import FastAPI
from ariadne.asgi import GraphQL
from app.api.graphql.schema import schema
from app.core.database import database

app = FastAPI()
graphql_app = GraphQL(schema, debug=True)

@app.get("/")
def read_root():
    return {"message": "User Profile Service is running"}

app.mount("/graphql", graphql_app)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()