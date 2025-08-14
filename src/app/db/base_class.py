# src/app/db/base_class.py
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import engine
from app.models import todo  # importa tus modelos

todo.Base.metadata.create_all(bind=engine)


Base = declarative_base()
