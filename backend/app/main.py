from fastapi import FastAPI
from app.routes import upload, assess, result, extract, agent

app = FastAPI()

app.include_router(upload.router)
app.include_router(assess.router)
app.include_router(result.router)
app.include_router(extract.router)  # Include the extract router
app.include_router(agent.router)

