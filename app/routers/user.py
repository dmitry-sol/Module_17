from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from app.backend.db_depends import get_db
from app.models import User
from app.schemas import CreateUser, UpdateUser
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])

# Получение всех активных пользователей
@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

# Получение пользователя по ID
@router.get('/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

# Создание нового пользователя
@router.post('/create')
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalar(select(User).where((User.username == user.username) | (User.slug == slugify(user.username))))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or slug already exists")

    stmt = insert(User).values(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.username))

    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

# Обновление информации о пользователе
@router.put('/update/{user_id}')
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalar(select(User).where(User.id == user_id))
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    stmt = update(User).where(User.id == user_id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age)

    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

# Удаление пользователя
@router.delete('/delete/{user_id}')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalar(select(User).where(User.id == user_id))
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    stmt = delete(User).where(User.id == user_id)

    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}
