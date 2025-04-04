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

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()
manager = websockets.manager

app = FastAPI(title=settings.APP_NAME)

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


@app.post("/api/users/register", response_model=schemas.Token)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
  """Register a new user"""
  db_user = auth.get_user(db, email=user_data.email)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")

  hashed_password = auth.get_password_hash(user_data.password)
  db_user = models.User(email=user_data.email, hashed_password=hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  session = auth.create_session(db, db_user.id)

  # Broadcast notification to all connected users
  await manager.broadcast(
      {"message": f"New user registered: {user_data.email}", "user_email": user_data.email},
      exclude_user=db_user.id
  )

  return auth.generate_login_response(db_user, session)


@app.post("/api/users/login", response_model=schemas.Token)
async def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
  user = auth.authenticate_user(db, form_data.email, form_data.password)
  if not user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
  session = auth.create_session(db, user.id)

  return auth.generate_login_response(user, session)

@app.post("/api/users/logout")
def logout(session: models = Depends(auth.get_current_session), db: Session = Depends(get_db)):
  """Logout user by invalidating the token"""
  if not session:
    raise HTTPException(status_code=400, detail="Invalid token")

  db.delete(session)
  db.commit()

  return {"message": "Logged out successfully"}

@app.post("/api/auth/refresh")
def refresh_token(session: models.Session = Depends(auth.get_current_session), db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == session.user_id).first()
  if not session or not user:
    raise HTTPException(status_code=400, detail="Invalid refresh token")

  # Generate new access token
  new_access_token = auth.create_access_token(data={"email": user.email})
  return {"access_token": new_access_token}

@app.get("/api/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
  """Get current user data"""
  return current_user


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
  """ Check is access token attached to the request """
  access_token = websocket.query_params.get("token")
  if not access_token:
    await websocket.close(code=1008, reason="Missing Token")
    return

  """Check if access token is valid"""
  try:
    user = auth.get_current_user(token=access_token, db=db)
    if not user:
      await websocket.close(code=1008, reason="Invalid Token")
      return
  except Exception as e:
    logger.error(f"Token validation error: {e}")
    await websocket.close(code=1008, reason="Invalid Token")
    return

  await manager.connect(websocket, user_id)
  try:
    while True:
      data = await websocket.receive_text()
      # We could process messages from clients here if needed
      logger.debug(f"Received message from user {user_id}: {data}")
  except WebSocketDisconnect:
    manager.disconnect(websocket, user_id)
  except Exception as e:
    logger.error(f"WebSocket error: {e}")
    manager.disconnect(websocket, user_id)