from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base  # ✅ misma Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
