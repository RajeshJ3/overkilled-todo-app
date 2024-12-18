from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# svc
from accounts_context import config


class SessionLocal:
    def __init__(self, engine):
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def __call__(self):
        db = self.db()
        try:
            yield db
        finally:
            db.close()


engine = create_engine(
    f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
)

db_dependency = SessionLocal(engine)
