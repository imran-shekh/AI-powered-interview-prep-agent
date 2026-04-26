from fastapi import FastAPI
from app.routes import extract, agent

app = FastAPI()

app.include_router(extract.router)  # Include the extract router
app.include_router(agent.router)

