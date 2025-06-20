from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base, Task

engine = create_engine("sqlite:///tasks.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_tasks():
    session = SessionLocal()
    task = session.query(Task).all()
    session.close()
    return task

def add_task(title, priority=2, done=False):
    session = SessionLocal()
    task = Task(title=title, priority=priority, done=done)
    session.add(task)
    session.commit()
    session.close()

def delete_task_by_id(task_id):
    session = SessionLocal()
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
    session.close()

def delete_task_by_index(index: int):
    session = SessionLocal()
    tasks = session.query(Task).order_by(Task.id).all()
    if 0 <= index < len(tasks):
        session.delete(tasks[index])
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
    tasks = session.query(Task).order_by(Task.done.asc()).all()
    session.close()
    return tasks

# def get_tasks_sorted():
#     session = SessionLocal()
#     tasks = session.query(Task).order_by(Task.done.asc(), Task.priority.desc().all())
#     session.close()
#     return tasks
