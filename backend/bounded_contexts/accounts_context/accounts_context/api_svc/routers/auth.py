from fastapi import APIRouter, Depends, status as http_status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import Annotated
from uuid import uuid4

# lib
from common_lib.hashing import get_hashed_password, check_password
from common_lib.jwt import get_access_token
from events_framework.utils.common_utils import event_message_builder
from events_framework.utils.rabbitmq_utils import publish_to_rabbitmq_queue

# svc
from accounts_context.api_svc.dependencies import verify_auth
from accounts_context.db.connection import db_dependency
from accounts_context.db.models import User
from accounts_context.utils.events.helpers import get_event_message_metadata
from accounts_context.utils.events.queues import Queue
from accounts_context.utils.events.types import EventType


class RegistrationPayload(BaseModel):
    full_name: str = "John Doe"
    email: EmailStr = "john.doe@example.com"
    password: str = "My$ecureP@$$w0rd"


class LoginPayload(BaseModel):
    email: EmailStr = "john.doe@example.com"
    password: str = "My$ecureP@$$w0rd"


security = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registration/")
async def registration(
    payload: RegistrationPayload, db: Session = Depends(db_dependency)
):
    uid = uuid4()
    # email should always be in lower case
    payload.email = payload.email.lower()

    # check if user exists with this email
    qs = db.query(User).filter(User.email == payload.email)
    if qs.count():
        content = {"details": "user with this email already exists!"}
        return JSONResponse(content, status_code=http_status.HTTP_400_BAD_REQUEST)

    # validate password
    if payload.password.__len__() < 6:
        content = {"details": "password must be atleast 6 characters long"}
        return JSONResponse(content, status_code=http_status.HTTP_400_BAD_REQUEST)

    # hash password
    payload.password = get_hashed_password(payload.password)

    payload_dict = {
        "id": uid.__str__(),
        "full_name": payload.full_name,
        "email": payload.email,
        "password": payload.password,
    }

    user = User(**payload_dict)
    db.add(user)
    db.commit()

    # publish message to a queue/topic
    message_payload = {
        "id": user.id.__str__(),
        "full_name": user.full_name,
        "email": user.email,
    }
    message_dict = event_message_builder(
        message_payload, EventType.USER_REGISTERED, meta=get_event_message_metadata()
    )
    await publish_to_rabbitmq_queue(message_dict, Queue.USERS)

    # get access_token
    to_encode = {"user_id": user.id.__str__()}
    access_token = get_access_token(to_encode)

    content = {
        "access_token": access_token,
        "user": {
            "id": user.id.__str__(),
            "full_name": user.full_name,
            "email": user.email,
        },
    }

    return JSONResponse(content, status_code=http_status.HTTP_201_CREATED)


@router.post("/login/")
async def login(payload: LoginPayload, db: Session = Depends(db_dependency)):
    # check if user exists with this email
    qs = db.query(User).filter(User.email == payload.email)
    users = qs.all()

    if not users.__len__():
        content = {"details": "user with this email does not exist!"}
        return JSONResponse(content, status_code=http_status.HTTP_400_BAD_REQUEST)

    user: User = users[0]

    # verify password
    if not check_password(payload.password, user.password):
        content = {"details": "incorrect password"}
        return JSONResponse(content, status_code=http_status.HTTP_400_BAD_REQUEST)

    # get access_token
    to_encode = {"user_id": user.id.__str__()}
    access_token = get_access_token(to_encode)

    content = {
        "access_token": access_token,
        "user": {
            "id": user.id.__str__(),
            "full_name": user.full_name,
            "email": user.email,
        },
    }

    return JSONResponse(content, status_code=http_status.HTTP_200_OK)


@router.get("/verify/")
async def verify(_: Annotated[None, Depends(verify_auth)]):
    return JSONResponse({}, status_code=http_status.HTTP_200_OK)
