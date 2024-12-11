from sqlalchemy.dialects.mysql import insert
from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from backend.db import *
from models.models import Post, User
from schemas import CreatePost, UpdatePost

router = APIRouter(prefix="/post", tags=['post'])


@router.get("/all_posts")
async def get_all_posts(db: Annotated[Session, Depends(get_db)]):
    stmt = select(Post)
    result = db.execute(stmt)
    posts = result.scalars().all()
    if not posts:
        raise HTTPException(status_code=404, detail="Нет доступных постов")
    return {"posts": posts}


@router.post("/create_post")
async def create_post(create_post: CreatePost, db: Annotated[Session, Depends(get_db)]):
    author_id = create_post.author_id

    # Проверка, существует ли автор
    existing_author =db.scalar(select(User).where(User.id==author_id))
    if existing_author is None:
        raise HTTPException(status_code=404, detail="Авто не найден")

    # Создание нового поста
    new_post = insert(Post).values(
        title=create_post.title,
        content=create_post.content,
        author_id=author_id,
    )
    db.add(new_post)
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Post created successfully'}


@router.put("/update_post/{author_id}")
async def update_post(user_id: int, update_post: UpdatePost, db: Annotated[Session, Depends(get_db)]):
    post = db.scalars(select(Post).where(Post.user_id==user_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    db.execute(update(Post).where(Post.user_id==user_id).values(
        title=update_post.title,
        content=update_post.content,
    ))
    db.commit()
    return {'status_code': status.HTTP_200_OK,'transaction': 'Post updated successfully'}

@router.delete("/delete_post/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.scalars(select(Post).where(Post.user_id==post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    db.execute(delete(Post).where(Post.user_id==post_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,'transaction': 'Post delete is successful'}
