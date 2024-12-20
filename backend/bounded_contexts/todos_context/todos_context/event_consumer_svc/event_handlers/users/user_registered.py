import logging

from sqlalchemy.orm.session import Session

from todos_context.db.models import User


def handle_user_registered(payload: dict, db: Session) -> bool:
    payload: dict = payload["payload"]

    payload_dict = {
        "id": payload["id"],
        "full_name": payload["full_name"],
    }

    user = User(**payload_dict)
    db.add(user)
    db.commit()

    logging.info("[handle_user_registered] new user created ✅")

    return True
