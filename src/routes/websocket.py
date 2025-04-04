import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketDisconnect

from src import websockets, auth
from src.database import get_db
from src.websockets import manager

router = APIRouter()
manager = websockets.manager
logger = logging.getLogger(__name__)

@router.websocket("/ws/{user_id}")
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
