from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .schema import schema

app = FastAPI(title="tallybook")
app.include_router(GraphQLRouter(schema), prefix="/graphql")
