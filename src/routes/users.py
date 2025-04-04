from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import models, schemas, auth, websockets
from src.database import get_db

router = APIRouter()
manager = websockets.manager

@router.post("/api/users/register", response_model=schemas.Token)
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


@router.post("/api/users/login", response_model=schemas.Token)
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

@router.post("/api/users/logout")
def logout(session: models = Depends(auth.get_current_session), db: Session = Depends(get_db)):
  """Logout user by invalidating the token"""
  if not session:
    raise HTTPException(status_code=400, detail="Invalid token")

  db.delete(session)
  db.commit()

  return {"message": "Logged out successfully"}

@router.post("/api/auth/refresh")
def refresh_token(session: models.Session = Depends(auth.get_current_session), db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == session.user_id).first()
  if not session or not user:
    raise HTTPException(status_code=400, detail="Invalid refresh token")

  # Generate new access token
  new_access_token = auth.create_access_token(data={"email": user.email})
  return {"access_token": new_access_token}

@router.get("/api/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
  """Get current user data"""
  return current_user
