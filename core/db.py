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
