from typing import Optional

from pydantic import BaseModel
from auth.apps.users.documents import Post


class PostModel(BaseModel):
    created_by: Optional[str]
    item: str
    desc: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(Post):
    hashed_password: str


class CommentModel(BaseModel):
    com: str
    current_user: Optional[str]
