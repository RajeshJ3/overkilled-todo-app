from fastapi import APIRouter, Depends, Request, status as http_status
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import uuid4

# svc
from teams_context.api_svc.dependencies import verify_auth_user
from teams_context.db.connection import db_dependency
from teams_context.db.models import User, Team, Member


class CreateTeamPayload(BaseModel):
    name: str = "My First Team"


router = APIRouter(
    prefix="",
    tags=["teams"],
    dependencies=[Depends(verify_auth_user)],
)


@router.get("/list")
async def list_teams(request: Request, db: Session = Depends(db_dependency)):

    stmt = (
        select(Team)
        .join(Member, Team.id == Member.team)
        .filter(Member.user == request.state.user_id)
    )
    qs = db.scalars(stmt).all()

    data = [
        {
            "id": i.id.__str__(),
            "name": i.name,
        }
        for i in qs
    ]

    return JSONResponse(data, status_code=http_status.HTTP_200_OK)


@router.get("/{id}")
async def get_team(id: str, request: Request, db: Session = Depends(db_dependency)):

    stmt = (
        select(Team)
        .join(Member, Team.id == Member.team)
        .filter(Member.user == request.state.user_id)
        .filter(Team.id == id)
    )
    team: Team = db.scalars(stmt).first()

    stmt = (
        select(Member.id, User)
        .join(User, Member.user == User.id)
        .filter(Member.team == team.id)
    )
    members = db.execute(stmt).all()

    data = {
        "id": team.id.__str__(),
        "name": team.name,
        "members": [
            {
                "id": member[0].__str__(),
                "user": {
                    "id": member[1].id.__str__(),
                    "full_name": member[1].full_name,
                },
            }
            for member in members
        ],
    }
    return JSONResponse(data, status_code=http_status.HTTP_200_OK)


@router.post("/create")
async def create_team(
    request: Request, payload: CreateTeamPayload, db: Session = Depends(db_dependency)
):
    user_id: str = request.state.user_id

    team_uid = uuid4()

    team_payload = {
        "id": team_uid.__str__(),
        "name": payload.name,
    }

    team = Team(**team_payload)
    db.add(team)
    db.commit()

    member_uid = uuid4()
    member_payload = {
        "id": member_uid.__str__(),
        "user": user_id,
        "team": team_uid,
    }

    member = Member(**member_payload)
    db.add(member)
    db.commit()

    return JSONResponse(team_payload, status_code=http_status.HTTP_201_CREATED)
