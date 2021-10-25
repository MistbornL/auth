from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from beanie import PydanticObjectId
from typing import List

from fastapi.security import OAuth2PasswordRequestForm

from Todo.apps.users.documents import Post, User
from Todo.apps.users.services.auth import authenticate_user, create_access_token
from Todo.config import settings
from Todo.apps.users.models import Token

router = APIRouter(prefix="")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/create/post", status_code=201, response_model=Post)
async def register_user(item: Post):
    return await item.save()


@router.get("/api/get/post/{item_id}", response_model=Post)
async def register_user(item_id: str):
    if todo := await Post.find_one(Post.id == PydanticObjectId(item_id)):
        return todo


@router.post("/api/update/post/{item_id}", status_code=200, response_model=Post)
async def register_user(item_id: str, item: Post):
    if todo := await Post.find_one(Post.id == PydanticObjectId(item_id)):
        todo.item = item.item
        if item.comment:
            todo.desc = item.comment
        return await todo.save()
    raise HTTPException(status_code=400, detail="not found")


@router.post("/api/delete/post/{item_id}", response_model=Post)
async def delete_item(item_id: str):
    if todo := await Post.find_one(Post.id == PydanticObjectId(item_id)):
        return await Post.delete(todo)
    raise HTTPException(status_code=400, detail="not found")


