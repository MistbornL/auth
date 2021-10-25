from typing import List, Optional
from beanie import Document
from datetime import datetime


class User(Document):
    email: str
    password: str


class Post(Document):
    item: str
    comment: Optional[str]

