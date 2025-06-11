from app.entity.task import Task, Tasks
class TaskService:
    def __init__(self, repository):
        self.repository = repository

    async def get_tasks(self, filters=None)->Tasks:
        tasks = await self.repository.get_tasks(filters)
        return Tasks(tasks=[Task(**i.to_dict()) for i in tasks])
