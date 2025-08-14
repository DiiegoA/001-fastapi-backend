from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import crud, schemas

# Le ponemos un prefix para evitar el error en FastAPI
router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("", response_model=list[schemas.TodoRead])
@router.get("/", response_model=list[schemas.TodoRead], include_in_schema=False)
def list_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@router.post("", response_model=schemas.TodoRead)
@router.post("/", response_model=schemas.TodoRead, include_in_schema=False)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@router.put("/{todo_id}", response_model=schemas.TodoRead)
@router.put("/{todo_id}/", response_model=schemas.TodoRead, include_in_schema=False)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}", response_model=schemas.TodoRead)
@router.delete("/{todo_id}/", response_model=schemas.TodoRead, include_in_schema=False)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo no encontrado")
    return todo
