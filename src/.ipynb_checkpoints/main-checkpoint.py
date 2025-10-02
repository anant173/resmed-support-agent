import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# Import the new run_agent function
from src.agent.graph import run_agent

app = FastAPI(
    title="ResMed CPAP Troubleshooting Agent Backend",
    root_path=os.getenv("TFY_SERVICE_ROOT_PATH", ""),
    docs_url="/",
)

# CORS middleware for local development/different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
def status():
    return JSONResponse(content={"status": "OK"})


class UserInput(BaseModel):
    thread_id: str
    user_input: str


@app.post("/run_agent")
async def run_agent_endpoint(user_input: UserInput):
    """
    Receives user input and executes the ResMed agent to provide a response.
    """
    return await run_agent(user_input.thread_id, user_input.user_input)