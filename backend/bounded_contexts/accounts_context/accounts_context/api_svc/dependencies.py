from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from datetime import datetime
from sqlalchemy.orm import Session
from typing import Annotated

# lib
from common_lib.jwt import decode_access_token

# svc
from accounts_context.db.connection import db_dependency
from accounts_context.db.models import User


security = HTTPBearer()


async def _verify_token(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(db_dependency),
    append_user: bool = False,
):
    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("user_id", None)
    exp = payload.get("exp", None)

    now = datetime.now().timestamp().__int__()

    # validate password expiry
    if now > exp:
        raise HTTPException(status_code=401, detail="access token is expired")

    # append user, only if requested
    if append_user:
        user: User = db.query(User).get(user_id)
        request.state.user = user


async def verify_auth(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(db_dependency),
):
    await _verify_token(request, credentials, db, append_user=False)


async def verify_auth_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(db_dependency),
):
    await _verify_token(request, credentials, db, append_user=True)
