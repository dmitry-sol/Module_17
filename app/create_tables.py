from app.backend.db import engine, Base
from app.models.task import Task
from app.models.user import User

Task.__table__.create(engine, checkfirst=True)
User.__table__.create(engine, checkfirst=True)
