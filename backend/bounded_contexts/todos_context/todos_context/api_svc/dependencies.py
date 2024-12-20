from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session
from typing import Annotated

# svc
from todos_context.db.connection import db_dependency
from todos_context.db.models import User


security = HTTPBearer()


async def _verify_token(
    request: Request,
    db: Session = Depends(db_dependency),
    append_user: bool = False,
):
    user_id = request.headers.get("X-User-ID")

    request.state.user_id = user_id

    # append user, only if requested
    if append_user:
        user: User = db.query(User).get(user_id)
        request.state.user = user


async def verify_auth(
    request: Request,
    _: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(db_dependency),
):
    await _verify_token(request, db, append_user=False)


async def verify_auth_user(
    request: Request,
    _: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(db_dependency),
):
    await _verify_token(request, db, append_user=True)
