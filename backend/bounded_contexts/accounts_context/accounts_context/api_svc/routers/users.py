from fastapi import APIRouter, Depends, Request, status as http_status
from fastapi.responses import JSONResponse

# svc
from accounts_context.api_svc.dependencies import verify_auth_user
from accounts_context.db.models import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_auth_user)],
)


@router.get("")
async def get_current_user(request: Request):
    user: User = request.state.user

    content = {
        "id": user.id.__str__(),
        "full_name": user.full_name,
        "email": user.email,
    }
    return JSONResponse(content, status_code=http_status.HTTP_200_OK)
