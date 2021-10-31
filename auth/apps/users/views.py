from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from beanie import PydanticObjectId
from typing import List

from fastapi.security import OAuth2PasswordRequestForm

from auth.apps.users.documents import Post, User, Comment
from auth.apps.users.services.auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from auth.config import settings
from auth.apps.users.models import Token

router = APIRouter(prefix="")


@router.post("/signup")
async def signup(user_data: User):
    user_data.password = get_password_hash(user_data.password)
    await user_data.save()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/create/post", status_code=201, response_model=Post)
async def create_post(item: Post, current_user: User = Depends(get_current_user)):
    item.created_by = str(current_user.email)
    return await item.save()


@router.get("/api/get/post/{item_id}", response_model=Post)
async def get_post(item_id: str):
    if post := await Post.get(item_id):
        return post
    raise HTTPException(status_code=400, detail="not found")


@router.get("/api/get/all/post")
async def find_all_post():
    return await Post.find_all().to_list()


@router.get("/", response_model=List[Post])
async def get_last_ten_post(limit: int = 3):
    post = await Post.find_all().limit(limit).to_list()
    return post


@router.post("/api/update/post/{item_id}", status_code=200, response_model=Post)
async def register_user(item_id: str, new_item: str, current_user: User = Depends(get_current_user)):
    if post := await Post.get(item_id):
        if post.created_by == str(current_user.email):
            post.item = new_item
            return await post.save()
    raise HTTPException(status_code=400, detail="not found")


@router.post("/api/delete/post/{item_id}", response_model=Post)
async def delete_item(item_id: str, current_user: User = Depends(get_current_user)):
    if post := await Post.get(item_id):
        if str(current_user.email) == post.created_by:
            return await Post.delete(post)
    raise HTTPException(status_code=400, detail="not found")


@router.post("/api/create/comment/{item_id}", status_code=201, response_model=Comment)
async def create_comment(item_id: str, item: Comment, current_user: User = Depends(get_current_user)):
    if post := await Post.get(item_id):
        item.current_user = str(current_user.email)
        return await item.save()


@router.post("/api/update/comment/{comment_id}", status_code=200, response_model=Comment)
async def update_comment(comment_id: str, item: Comment, new_comment: str, current_user: User = Depends(get_current_user)):
    if com := await Comment.get(comment_id):
        item.com = new_comment
        item.current_user = str(current_user.email)
        return await item.save()
    raise HTTPException(status_code=400, detail="not found")


@router.post("/api/delete/comment/{comment_id}", response_model=Comment)
async def delete_item(comment_id: str):
    if com := await Comment.get(comment_id):
        return await Comment.delete(com)
    raise HTTPException(status_code=400, detail="not found")


@router.get("/api/get/comment/{comment_id}", response_model=Comment)
async def get_comment(comment_id: str):
    if com := await Comment.get(comment_id):
        return com
    raise HTTPException(status_code=400, detail="not found")


@router.get("/api/get/all/comment/", response_model=List[Comment])
async def get_comment():
    return await Comment.find_all().to_list()
