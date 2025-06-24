from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from core.models import Base, Task

engine = create_engine("sqlite:///tasks.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_tasks():
    session = SessionLocal()
    task = session.query(Task).order_by(Task.position).all()
    session.close()
    return task

def get_task_by_id(task_id: int):
    session = SessionLocal()
    task = session.query(Task).get(task_id)
    session.close()
    return task

def add_task(title, priority=2, done=False):
    session = SessionLocal()
    max_position = session.query(func.max(Task.position)).scalar()
    if max_position is None:
        max_position = 0
    new_task = Task(title=title, priority=priority, done=done, position=max_position + 1)
    session.add(new_task)
    session.commit()
    session.close()

def delete_task_by_id(task_id):
    session = SessionLocal()
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
    session.close()

def update_task(task_id: int, title: str = None, priority: int = None, done: bool = None):
    session = SessionLocal()
    task = session.query(Task).get(task_id)
    if task:
        if title is not None:
            task.title = title
        if priority is not None:
            task.priority = priority
        if done is not None:
            task.done = done
        session.commit()
    session.close()

def toggle_task_done(task_id):
    session = SessionLocal()
    task = session.query(Task).get(task_id)
    if task:
        task.done = not task.done
        session.commit()
    session.close()

def clear_all_tasks():
    session = SessionLocal()
    session.query(Task).delete()
    session.commit()
    session.close()

def sort_tasks_by_status():
    session = SessionLocal()
    tasks = session.query(Task).order_by(Task.done.asc(), Task.position.asc()).all()
    for index, task in enumerate(tasks):
        task.position = index

    session.commit()

    sorted_tasks = session.query(Task).order_by(Task.position.asc()).all()

    detached_tasks = [Task(title=task.title, priority=task.priority, done=task.done) for task in sorted_tasks]
    for index, task in enumerate(detached_tasks):
        task.id = sorted_tasks[index].id
        task.position = sorted_tasks[index].position

    session.close()
    return detached_tasks
