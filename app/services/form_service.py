from typing import Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.form_dto import (CreateFormRequest, UpdateFormRequest)
from app.models.form import FormData
from app.models.user import UserData
from fastapi import HTTPException, status

class FormService:
    async def list(self):
        query_task = FormData.find_all()
        total = await query_task.count()
        form_list = await query_task.to_list()
        forms_dict = []
        for form in form_list:
            form_dict = form.dict()
            forms_dict.append(form_dict)
            
        return forms_dict, total


    async def post(
        self,
        form_input: CreateFormRequest
    ):
        form_dict = form_input.dict()
        model = FormData(**form_dict)
        await model.save()
        return model.dict()


    async def put(
        self,
        form_input: UpdateFormRequest
    ):        
        form = await FormData.find_one({'_id': PydanticObjectId(form_input.id)})
        if not form:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Bài đăng không tồn tại')
        
        await form.update({"$set": {
            "question" : form_input.question,
            "answers" : form_input.answers,
            "weight" : form_input.weight,
            "form_type" : form_input.form_type,
            "matrix" : form_input.matrix
        }})
        
        return form.dict()
    
    
    async def delete(
        self,
        form_id: str
    ):
        form = await FormData.find_one({'_id': PydanticObjectId(form_id)})
        if not form:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Câu hỏi không tồn tại')

        await form.delete()