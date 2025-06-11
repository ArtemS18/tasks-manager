from typing import List
from pydantic import BaseModel
from app.entity.task import Task, Tasks

class TaskSchema(Task):
    pass


class TasksSchema(Tasks):
    pass
