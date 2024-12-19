from fastapi import FastAPI

# svc
from teams_context.api_svc.routers.users import router as users_router
from teams_context.api_svc.routers.teams import router as teams_router

app = FastAPI(root_path="/teams")

app.include_router(users_router)
app.include_router(teams_router)


@app.get("/health_check", tags=["health_check"])
async def health_check():
    return {"details": "ok 🚀"}
