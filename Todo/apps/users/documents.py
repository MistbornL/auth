from typing import List, Optional
from beanie import Document
from datetime import datetime


class User(Document):
    email: str
    password: str


class Post(Document):
    item: str
    desc: Optional[str]


class Comment(Document):
    item: str
    created_by: str


