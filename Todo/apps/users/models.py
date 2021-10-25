from typing import Optional

from pydantic import BaseModel
from Todo.apps.users.documents import Post


class TodoItem(BaseModel):
    item: str
    desc: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(Post):
    hashed_password: str
