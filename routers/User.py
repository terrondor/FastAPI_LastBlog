from fastapi import APIRouter, Depends, HTTPException,  status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
from backend.db import *
from models.models import User
from schemas import CreateUser, UpdateUser
from typing import Annotated
from sqlalchemy import select, update, delete
from security import *
from templates import templates


router = APIRouter(prefix="/user", tags=['user'])


@router.get("/all_users")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    stmt = select(User)
    result =  db.execute(stmt)
    users = result.scalars().all()
    if users is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Пользователи не найдены")
    return list(users)



@router.post("/create_user")
async def create_user(request:Request, create_user: CreateUser,
                      db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    # Проверка совпадения паролей
    if create_user.password != create_user.confirm_password:
        return templates.TemplateResponse("register.html", {request: request, "error": "Пароли не совпадают"})

    # Проверка существующего пользователя
    existing_user_result = db.execute(select(User).where(User.username == create_user.username))
    existing_user = existing_user_result.scalar_one_or_none()
    if existing_user:
        return templates.TemplateResponse("register.html", {request: request, "error": "Имя пользователя уже занято"})

    # Проверка существующего email
    existing_email_result = db.execute(select(User).where(User.email == create_user.email))
    existing_email = existing_email_result.scalar_one_or_none()
    if existing_email:
        return templates.TemplateResponse("register.html", {request: request, "error":"Email уже зарегистрирован"})

    # Хэширование пароля
    hashed_password = pwd_context.hash(create_user.password)

    # Вставка нового пользователя
    stmt = insert(User).values(
        username=create_user.username,
        email=create_user.email,
        password=hashed_password,
    )

    db.execute(stmt)
    db.commit()

    return RedirectResponse(url="register.html", status_code=303)


@router.put("/update_user/{user_id}")
async def update_user(user_id: int, update_user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    user = db.scalars(select(User).where(User.id==user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db.execute(update(User).where(User.id==user_id).values(
        username=update_user.username,
        email=update_user.email,
        password=update_user.password,
    ))
    db.commit()
    return {"status": "success"}


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Найти пользователя по ID
    user = db.scalars(select(User).where(User.id==user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


    # Удалить пользователя из базы данных
    db.execute(delete(User).where(User.id==user_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK,'transaction': 'User delete is successful'}
