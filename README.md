# Schedo

Schedo is a simple demo task scheduling and processing system built with FastAPI and Celery.

## Features

- **FastAPI-powered REST API** for task submission and monitoring
- **Asynchronous task processing** with Celery
- **Priority queuing** support for high-priority tasks
- **Task monitoring** with detailed status tracking
- **Scheduled tasks** for automated processing
- **Health checks** and system monitoring
- **Docker support** for easy deployment
- **Scalable architecture** with separate workers for different priorities

## Tech Stack

- Python 3.12+
- FastAPI
- Celery
- Redis (message broker and result backend)
- Flower (for Celery monitoring)
- Docker & Docker Compose
- UV (Python package installer and runner)

## API Endpoints

### Submit Task for Processing

```http
POST /process
```

Request body:

```json
{
  "data_id": "string",
  "priority": "normal"
}
```

### Get Task Status

```http
GET /task/{task_id}
```

Returns detailed task information including status, result, and execution details.

## Task Types

1. **Data Processing Tasks**
    - Normal priority processing
    - High priority processing (separate queue)
    - Configurable retries and delays

2. **Scheduled Tasks**
    - Daily report generation
    - Hourly data processing
    - System health checks

## Configuration

Environment variables:

- `CELERY_BROKER_URL`: Redis broker URL (default: "redis://localhost:6379/0")
- `CELERY_RESULT_BACKEND`: Redis result backend URL (default: "redis://localhost:6379/0")
- `CELERY_WORKER_CONCURRENCY`: Number of worker processes (default: 4)

## Installation and Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ozcanyarimdunya/schedo.git
   cd schedo
   ```

2. **Using Docker (recommended)**
   ```bash
   docker-compose up -d
   ```
   This will start:
    - FastAPI application (port 8000)
    - Redis instance
    - Normal priority worker
    - High priority worker
    - Celery beat scheduler
    - Flower monitoring interface (port 5555)

3. **Local Development Setup**
   ```bash
   # Create a virtual environment
   uv init
   
   # Install dependencies
   uv sync
   
   # Run the application
   uvicorn schedo.main:app --reload
   
   # Run Celery worker
   celery -A schedo.tasks worker --loglevel=info
   ```

## Architecture

The system consists of several components:

- **API Server**: Handles incoming requests and task submission
- **Redis**: Acts as message broker and result backend
- **Normal Priority Worker**: Processes regular tasks
- **High Priority Worker**: Dedicated to high-priority tasks
- **Beat Scheduler**: Manages scheduled tasks
- **Flower**: Provides monitoring interface

## License

[Your chosen license]