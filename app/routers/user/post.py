from fastapi import APIRouter, Query, Depends
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.post_dto import (CreatePostRequest, UpdatePostRequest)
from app.services.post_service import PostService
from app.helpers.jwt_helpers import generate_token, require_user, decode_token
from app.models.post import PostData
from beanie import PydanticObjectId
from typing import Union, Annotated

route = APIRouter(tags=['Post'], prefix="/post")

@route.get('/detail/{post_id}')
async def get_list_post_data(post_id: str):
    item = await PostData.find_one({'_id': PydanticObjectId(post_id)})
    
    return {
        "message": "Chi tiết bài đăng",
        "data": item,
    }

@route.get('/list/{post_status}')
async def get_list_post_data(post_status: str):
    items, total = await PostService().list(post_status)
    
    return {
        "message": "Lấy danh sách thành công",
        "data": items,
        "total": total
    }

@route.post('')
async def create_post(post_input: CreatePostRequest, user_id: str = Depends(require_user)):
    posts = await PostService().post(post_input, user_id)
    return {
        "message": "Tạo bài đăng thành công",
        "data": posts
    }


@route.put('')
async def update_post(post_input: UpdatePostRequest, user_id: str = Depends(require_user)):
    posts = await PostService().put(post_input, user_id)
    return {
        "message": "Cập nhật bài đăng thành công",
        "data": posts
    }
