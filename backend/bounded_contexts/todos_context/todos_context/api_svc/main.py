from fastapi import FastAPI

# svc
from todos_context.api_svc.routers.users import router as users_router
from todos_context.api_svc.routers.todos import router as todos_router

app = FastAPI(root_path="/todos")

app.include_router(users_router)
app.include_router(todos_router)


@app.get("/health_check", tags=["health_check"])
async def health_check():
    return {"details": "ok 🚀"}
