from app.db.base_class import Base
from app.db.session import engine
from app.models import todo  # importa tus modelos aquí

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
