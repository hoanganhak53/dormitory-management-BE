from typing import Optional
from datetime import datetime
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, Eq
from app.dto.thesis_data_dto import ThesisDataCreateRequest, ShortThesisData, FullThesisData
from app.models.thesis_data import ThesisData

class ThesisDataService:
    async def list(
        self,
        title: Optional[str],
        semester: Optional[str],
        created_at: Optional[datetime],
        page: int = 1,
        limit: int = 10,
    ):
        query = []
        skip = limit * (page - 1)
        if title:
            query.append(RegEx(ThesisData.title, title, options="i"))
        if semester:
            query.append(Eq(ThesisData.semester, semester))
        if created_at:
            query.append(GTE(ThesisData.created_at, created_at))
        query_task = ThesisData.find_many(*query)
        total = await query_task.count()
        thesis_data_list = await query_task.skip(skip).limit(limit).project(ShortThesisData).to_list()
        return thesis_data_list, total

    async def get(
        self,
        thesis_id: str
    ):
        thesis_data = await ThesisData.find_one({'_id': PydanticObjectId(thesis_id)}).project(FullThesisData)
        if not thesis_data:
            # Exception module is not implemented so we use this
            raise Exception("No thesis")
        return thesis_data

    async def create(
        self,
        thesis_input: ThesisDataCreateRequest,
    ):
        thesis_dict = thesis_input.dict()
        model = ThesisData(**thesis_dict)
        await model.save()
        return str(model.id)

    async def delete(
        self,
        thesis_id: str
    ):
        thesis = await ThesisData.find_one({'_id': PydanticObjectId(thesis_id)})
        if not thesis:
            raise Exception("No thesis")
        await thesis.delete()