from pydantic import BaseModel


class CreatePost(BaseModel):
    title: str
    content: str
    author_id: int


class CreateUser(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class UpdateUser(BaseModel):
    username: str
    email: str
    password: str


class UpdatePost(BaseModel):
    title: str
    content: str
    author_id: int
