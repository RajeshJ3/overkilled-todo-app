from fastapi import APIRouter, Depends, Request, status as http_status
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import uuid4

# svc
from todos_context.api_svc.dependencies import verify_auth_user
from todos_context.db.connection import db_dependency
from todos_context.db.models import TodoCategory, Todo


class CreateTodoCategoryPayload(BaseModel):
    name: str


class CreateTodoPayload(BaseModel):
    title: str
    category_id: str
    is_completed: bool = False
    description: str = None


router = APIRouter(
    prefix="",
    tags=["todos"],
    dependencies=[Depends(verify_auth_user)],
)


@router.get("/categories/list")
async def list_todo_categories(request: Request, db: Session = Depends(db_dependency)):

    qs = (
        db.query(TodoCategory)
        .filter(
            TodoCategory.user == request.state.user_id, TodoCategory.is_deleted == False
        )
        .all()
    )

    data = [
        {
            "id": i.id.__str__(),
            "name": i.name,
        }
        for i in qs
    ]

    return JSONResponse(data, status_code=http_status.HTTP_200_OK)


@router.post("/categories/create")
async def create_todo_category(
    request: Request,
    payload: CreateTodoCategoryPayload,
    db: Session = Depends(db_dependency),
):
    uid = uuid4()

    todo_category_payload = {
        "id": uid.__str__(),
        "user": request.state.user_id,
        "name": payload.name,
    }

    todo_category = TodoCategory(**todo_category_payload)
    db.add(todo_category)
    db.commit()

    content = {
        "id": todo_category_payload["id"],
        "name": todo_category_payload["name"],
    }

    return JSONResponse(content, status_code=http_status.HTTP_201_CREATED)


@router.put("/categories/{id}")
async def update_category(
    id: str,
    request: Request,
    payload: CreateTodoCategoryPayload,
    db: Session = Depends(db_dependency),
):

    category_qs = db.query(TodoCategory).filter(
        TodoCategory.user == request.state.user_id,
        TodoCategory.id == id,
        TodoCategory.is_deleted == False,
    )

    todo_category_payload = {
        "name": payload.name,
    }

    category_qs.update(todo_category_payload)
    db.commit()

    return JSONResponse(todo_category_payload, status_code=http_status.HTTP_201_CREATED)


@router.delete("/categories/{id}")
async def delete_category(
    id: str,
    request: Request,
    db: Session = Depends(db_dependency),
):

    category_qs = db.query(TodoCategory).filter(
        TodoCategory.user == request.state.user_id,
        TodoCategory.id == id,
        TodoCategory.is_deleted == False,
    )

    todo_category_payload = {
        "is_deleted": True,
    }

    category_qs.update(todo_category_payload)
    db.commit()

    return JSONResponse({}, status_code=http_status.HTTP_200_OK)


@router.get("/list")
async def list_todos(
    category_id: str, request: Request, db: Session = Depends(db_dependency)
):

    category = (
        db.query(TodoCategory)
        .filter(
            TodoCategory.user == request.state.user_id,
            TodoCategory.id == category_id,
            TodoCategory.is_deleted == False,
        )
        .first()
    )

    todos = (
        db.query(Todo)
        .filter(Todo.category == category.id, Todo.is_deleted == False)
        .all()
    )

    data = [
        {
            "id": i.id.__str__(),
            "title": i.title,
            "description": i.description,
            "is_completed": i.is_completed,
        }
        for i in todos
    ]

    return JSONResponse(data, status_code=http_status.HTTP_200_OK)


@router.post("/create")
async def create_todo(
    request: Request, payload: CreateTodoPayload, db: Session = Depends(db_dependency)
):
    categories = (
        db.query(TodoCategory)
        .filter(
            TodoCategory.id == payload.category_id,
            TodoCategory.user == request.state.user_id,
            TodoCategory.is_deleted == False,
        )
        .count()
    )

    if not categories:
        return JSONResponse({}, status_code=http_status.HTTP_404_NOT_FOUND)

    uid = uuid4()

    todo_payload = {
        "id": uid.__str__(),
        "category": payload.category_id,
        "title": payload.title,
        "is_completed": payload.is_completed,
        "description": payload.description,
    }

    todo = Todo(**todo_payload)
    db.add(todo)
    db.commit()

    return JSONResponse(todo_payload, status_code=http_status.HTTP_201_CREATED)


@router.put("/{id}")
async def update_todo(
    id: str,
    payload: CreateTodoPayload,
    request: Request,
    db: Session = Depends(db_dependency),
):

    todo_qs = db.query(Todo).filter(
        Todo.id == id,
        Todo.is_deleted == False,
    )

    todo = todo_qs.first()
    if not todo:
        return JSONResponse({}, status_code=http_status.HTTP_404_NOT_FOUND)

    categories = (
        db.query(TodoCategory)
        .filter(
            TodoCategory.id == todo.category,
            TodoCategory.user == request.state.user_id,
            TodoCategory.is_deleted == False,
        )
        .count()
    )

    if not categories:
        return JSONResponse({}, status_code=http_status.HTTP_404_NOT_FOUND)

    todo_payload = {
        "title": payload.title,
        "category": payload.category_id,
        "is_completed": payload.is_completed,
        "description": payload.description,
    }

    todo_qs.update(todo_payload)
    db.commit()

    return JSONResponse({}, status_code=http_status.HTTP_200_OK)


@router.delete("/{id}")
async def delete_todo(id: str, request: Request, db: Session = Depends(db_dependency)):

    todo_qs = db.query(Todo).filter(
        Todo.id == id,
        Todo.is_deleted == False,
    )

    todo = todo_qs.first()
    if not todo:
        return JSONResponse({}, status_code=http_status.HTTP_404_NOT_FOUND)

    categories = (
        db.query(TodoCategory)
        .filter(
            TodoCategory.id == todo.category,
            TodoCategory.user == request.state.user_id,
            TodoCategory.is_deleted == False,
        )
        .count()
    )

    if not categories:
        return JSONResponse({}, status_code=http_status.HTTP_404_NOT_FOUND)

    todo_payload = {
        "is_deleted": True,
    }

    todo_qs.update(todo_payload)
    db.commit()

    return JSONResponse({}, status_code=http_status.HTTP_200_OK)
