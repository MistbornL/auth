from typing import List, Optional
from beanie import Document
from datetime import datetime




class User(Document):
    email: str
    password: str


class Comment(Document):
    com: Optional[str]
    current_user: Optional[str]


class Post(Document):
    created_by: Optional[str]
    item: str
    desc: Optional[str]
