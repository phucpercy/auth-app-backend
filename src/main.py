import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from src import models
from src import schemas
from src import auth
from src import websockets
from src.database import engine, get_db, Base
from src.config import get_settings
from src.routes import websocket, users

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/api/health")
async def health_check():
  return {"status": "ok"}

app.include_router(users.router)
app.include_router(websocket.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)