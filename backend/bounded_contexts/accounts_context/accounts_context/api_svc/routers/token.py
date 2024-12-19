from fastapi import APIRouter, Depends, HTTPException, status as http_status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from datetime import datetime
from typing import Annotated

# lib
from common_lib.jwt import decode_access_token

security = HTTPBearer()
router = APIRouter(prefix="/token", tags=["token"])


@router.get("/verify/")
async def verify(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("user_id", None)
    exp = payload.get("exp", None)

    now = datetime.now().timestamp().__int__()

    # validate password expiry
    if now > exp:
        raise HTTPException(status_code=401, detail="access token is expired")

    headers = {"X-User-ID": user_id}
    return JSONResponse({}, status_code=http_status.HTTP_200_OK, headers=headers)
