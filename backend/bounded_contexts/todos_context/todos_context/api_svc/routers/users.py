from fastapi import APIRouter, Depends, Request, status as http_status
from fastapi.responses import JSONResponse

# svc
from todos_context.api_svc.dependencies import verify_auth_user
from todos_context.db.models import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_auth_user)],
)


@router.get("/")
async def get_current_user(request: Request):
    user_id: str = request.state.user_id
    user: User = request.state.user

    content = {
        "user_id": user_id,
        "id": user.id.__str__(),
        "full_name": user.full_name,
    }
    return JSONResponse(content, status_code=http_status.HTTP_200_OK)
