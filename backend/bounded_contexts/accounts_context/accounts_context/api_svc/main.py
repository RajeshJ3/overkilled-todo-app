from fastapi import FastAPI

# svc
from accounts_context.api_svc.routers.auth import router as auth_router
from accounts_context.api_svc.routers.users import router as users_router


app = FastAPI(root_path="/accounts")

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", tags=["health_check"])
async def health_check():
    return {"details": "ok 🚀"}
