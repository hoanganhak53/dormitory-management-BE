from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.post_dto import (CreatePostRequest, UpdatePostRequest)
from app.models.post import PostData
from app.models.user import UserData
from fastapi import HTTPException, status

class PostService:
    async def list(self, post_status: str):
        if post_status == "all":
            query_task = PostData.find_all()
        else:
            query_task = PostData.find_many({'status': int(post_status)})
        
        total = await query_task.count()
        post_list = await query_task.to_list()
        posts_dict = []
        for post in post_list:
            post_dict = post.dict()
            user = await UserData.find_one({'_id': PydanticObjectId(post.user_id)})
            post_dict["created_user"] = user.full_name
            
            posts_dict.append(post_dict)
            
        return posts_dict, total


    async def post(
        self,
        post_input: CreatePostRequest,
        user_id: str
    ):
        post_dict = post_input.dict()
        post_dict['user_id'] = user_id        
        model = PostData(**post_dict)
        await model.save()
        return model.dict()


    async def put(
        self,
        post_input: UpdatePostRequest,
        user_id: str
    ):        
        post = await PostData.find_one({'_id': PydanticObjectId(post_input.id)})
        if not post:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Bài đăng không tồn tại')
        
        await post.update({"$set": {
            "image" : post_input.image,
            "title" : post_input.title,
            "content" : post_input.content,
            "status" : post_input.status
        }})
        
        return post.dict()