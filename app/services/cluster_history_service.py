from typing import Optional
from beanie import PydanticObjectId
from beanie.operators import RegEx
from app.dto.cluster_history_dto import ClusterHistoryPutRequest, ShortClusterHistory, FullClusterHistory
from app.models.cluster_history import ClusterHistory

class ClusterHistoryService:
    async def list(
        self,
        name: Optional[str],
        page: int = 1,
        limit: int = 10,
    ):
        query = []
        skip = limit * (page - 1)
        if name:
            query.append(RegEx(ClusterHistory.name, name, options="i"))
        query_task = ClusterHistory.find_many(*query)
        total = await query_task.count()
        cluster_history_list = await query_task.skip(skip).limit(limit).project(ShortClusterHistory).to_list()
        return cluster_history_list, total

    async def get(
        self,
        cluster_history_id: str
    ):
        cluster_history = await ClusterHistory.find_one({'_id': PydanticObjectId(cluster_history_id)}).project(FullClusterHistory)
        if not cluster_history:
            # Exception module is not implemented so we use this
            raise Exception("No cluster history")
        return cluster_history

    async def put(
        self,
        cluster_history_id: str,
        new_cluster_history: ClusterHistoryPutRequest,
    ):
        cluster_history = await ClusterHistory.find_one({'_id': PydanticObjectId(cluster_history_id)})
        if not cluster_history:
            raise Exception("No cluster history")
        await cluster_history.update(**new_cluster_history)
        return cluster_history

    async def delete(
        self,
        cluster_history_id: str
    ):
        cluster_history = await ClusterHistory.find_one({'_id': PydanticObjectId(cluster_history_id)})
        if not cluster_history:
            raise Exception("No cluster history")
        await cluster_history.delete()