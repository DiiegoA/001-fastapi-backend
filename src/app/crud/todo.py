from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from app.core.logging_config import logger

def get_todos(db: Session):
    logger.debug("Listando todos")
    return db.query(Todo).all()

def create_todo(db: Session, todo: TodoCreate):
    logger.info(f"Creando todo: {todo.name}")
    db_todo = Todo(name=todo.name, completed=todo.completed or False)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    logger.debug(f"Todo creado con ID: {db_todo.id}")
    return db_todo

def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None
    if todo_update.name is not None:
        todo.name = todo_update.name
    if todo_update.completed is not None:
        todo.completed = todo_update.completed
    db.commit()
    db.refresh(todo)
    logger.info(f"Todo {todo_id} actualizado")
    return todo

def delete_todo(db: Session, todo_id: int):
    logger.warning(f"Eliminando todo con ID: {todo_id}")
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        logger.info(f"Todo {todo_id} eliminado")
    else:
        logger.error(f"Intento de eliminar todo inexistente: {todo_id}")
    return todo
