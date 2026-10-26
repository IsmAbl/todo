from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.schemas.task import TaskSchema as ts, TaskCreate as tc, TaskUpdate as tu

class TaskNotFound(Exception):
    """"Couldn't found the task" in DB"""

class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db=db)

    def list_tasks(self) -> list[ts]:
        task_orm = self.task_repository.get_all()
        return [ts.model_validate(task) for task in task_orm]

    def create_task(self, task_create: tc) -> ts:
        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        return ts.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: tu) -> ts:
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f"Couldn't found the task - {task_id}")
        if task_update.title:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed  

        self.db.commit()
        return ts.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> ts:
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Couldn't found the task - {task_id}")
        self.task_repository.delete(task_for_delete)
        self.db.commit()