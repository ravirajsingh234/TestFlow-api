from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Task
from redis_client import check_redis_connection, redis_client
from schemas import TaskCreate, TaskResponse, TaskUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI(title="TestFlow API")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "redis": check_redis_connection()
    }


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    redis_client.delete("tasks")

    return new_task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    cached_tasks = redis_client.get("tasks")

    if cached_tasks:
        import json
        return json.loads(cached_tasks)

    tasks = db.query(Task).all()

    task_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat()
        }
        for task in tasks
    ]

    import json
    redis_client.setex(
        "tasks",
        60,
        json.dumps(task_data)
    )

    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.completed is not None:
        task.completed = task_data.completed

    db.commit()
    db.refresh(task)

    redis_client.delete("tasks")

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    redis_client.delete("tasks")

    return {
        "message": "Task deleted successfully"
    }
