import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from app.main import app
from app.models.todo import Todo
from app.db.session import engine, SessionLocal
from app.db.base_class import Base


# ----------- Configuración de BD de pruebas ------------
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    yield
    # Limpiar DB después de cada test
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos"))
        conn.commit()


# ----------- Cliente de pruebas -----------------------
@pytest.mark.asyncio
async def test_todo_crud():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Crear un Todo
        response = await ac.post("/todos/", json={"title": "Aprender FastAPI", "description": "Con SQLAlchemy"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Aprender FastAPI"
        assert "id" in data
        todo_id = data["id"]

        # 2. Listar Todos
        response = await ac.get("/todos/")
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 1
        assert todos[0]["id"] == todo_id

        # 3. Eliminar Todo
        response = await ac.delete(f"/todos/{todo_id}")
        assert response.status_code == 200
        deleted_todo = response.json()
        assert deleted_todo["id"] == todo_id

        # 4. Intentar eliminar nuevamente (debe fallar)
        response = await ac.delete(f"/todos/{todo_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo no encontrado"
