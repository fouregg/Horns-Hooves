from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.services.task import TaskService

router = APIRouter(tags=["Задачи"])


@router.get(path="/task/test", status_code=status.HTTP_200_OK)
async def test(task_service: Annotated[TaskService, Depends()]) -> None:
    """Тестовый эндпоинт для проверки работы сервиса задач."""
    return await task_service.test()
