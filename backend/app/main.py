from fastapi import FastAPI
from app.routes import extract, agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(extract.router)  # Include the extract router
app.include_router(agent.router)
