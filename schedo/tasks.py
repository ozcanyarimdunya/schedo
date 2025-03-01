import logging
import os
import time

from celery import Celery


logger = logging.getLogger(__name__)

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

app = Celery("tasks", broker=broker_url, backend=result_backend)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Istanbul",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    worker_concurrency=int(os.getenv("CELERY_WORKER_CONCURRENCY", 4)),
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_time_limit=10 * 60,
    task_soft_time_limit=500,
    broker_connection_retry_on_startup=True,
)

app.conf.beat_schedule = {
    "process_daily_report": {
        "task": "schedo.tasks.process_daily_report",
        "schedule": 86400.0,  # every 1 day
    },
    "process_hourly_data": {
        "task": "schedo.tasks.process_hourly_data",
        "schedule": 3600.0,  # every 1 hour
    },
    "check_system_health": {
        "task": "schedo.tasks.check_system_health",
        "schedule": 40.0,  # every 20 seconds
    },
}


@app.task(bind=True, max_retries=3, default_retry_delay=15)
def process_data(self, data_id: str):
    try:
        logger.info(f"Processing data with id: {data_id}")

        # Simulate data processing
        time.sleep(5)

        if int(data_id) % 10 == 0:
            raise Exception(f"Data processing failed for data_id: {data_id}")

        return {
            "status": "success",
            "data_id": data_id,
            "message": f"Data processed successfully for data_id: {data_id}",
            "result": {"data_id": data_id, "processed": True},
        }
    except Exception as exc:
        logger.error(f"Error while processing data_id {data_id}: {exc}")
        self.retry(exc=exc)


@app.task(bind=True, max_retries=5, default_retry_delay=60, queue="high_priority")
def process_high_priority_data(self, task_id: str):
    try:
        logger.info(f"Processing high priority task with id: {task_id}")

        # Simulate priority task
        time.sleep(3)

        return {
            "status": "success",
            "task_id": task_id,
            "message": f"High priority task processed successfully for task_id: {task_id}",
            "result": {"task_id": task_id, "processed": True},
        }
    except Exception as exc:
        logger.error(f"Error while processing high priority task_id {task_id}: {exc}")
        self.retry(exc=exc)


@app.task(bind=True, max_retries=3, default_retry_delay=300)
def process_daily_report(self):
    try:
        logger.info("Processing daily report")

        # Simulate daily report generation
        time.sleep(10)

        return {
            "status": "success",
            "message": "Daily report generated successfully",
            "result": {"generated": True},
        }
    except Exception as exc:
        logger.error(f"Error while generating daily report: {exc}")
        self.retry(exc=exc)


@app.task(bind=True, max_retries=3, default_retry_delay=120)
def process_hourly_data(self):
    try:
        logger.info("Processing hourly data")

        # Simulate hourly data processing
        time.sleep(8)

        return {
            "status": "success",
            "message": "Hourly data processed successfully",
            "result": {"processed": True},
        }
    except Exception as exc:
        logger.error(f"Error while processing hourly data: {exc}")
        self.retry(exc=exc)


@app.task(bind=True, max_retries=5, default_retry_delay=30)
def check_system_health(self):
    try:
        logger.info("Checking system health")

        # Simulate system health check
        time.sleep(3)

        return {
            "status": "success",
            "message": "System is healthy",
            "result": {"healthy": True, "timestamp": time.time()},
        }
    except Exception as exc:
        logger.error(f"Error while checking system health: {exc}")
        self.retry(exc=exc)
