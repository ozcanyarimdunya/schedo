import logging

from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from schedo.tasks import process_data
from schedo.tasks import process_high_priority_data


logger = logging.getLogger(__name__)

app = FastAPI()


class DataRequest(BaseModel):
    data_id: str
    priority: str = "normal"


@app.post("/process")
async def process(request: DataRequest):
    try:
        if request.priority == "high":
            task = process_high_priority_data.delay(request.data_id)
        else:
            task = process_data.delay(request.data_id)

        logger.info(message := f"Data processing task created with id {task.id} for data_id {request.data_id}")
        return {"message": message, "task_id": task.id}
    except Exception as exc:
        logger.error(f"Error while processing data: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    try:
        task: AsyncResult = process_data.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result,
            "info": task.info,
            "traceback": task.traceback,
            "name": task.name,
            "retries": task.retries,
            "queue": task.queue,
            "date_done": task.date_done,
        }
    except Exception as exc:
        logger.error(f"Error while getting task status for task_id {task_id}: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
