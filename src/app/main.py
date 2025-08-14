from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import todos
from app.exceptions import handlers
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging_config import logger

app = FastAPI(
    title="Todo API - FastAPI Backend",
    description="""
API para gestionar tareas (ToDos) construida con **FastAPI**, **SQLAlchemy**, **Alembic** y **PostgreSQL**.

## Endpoints principales:
- **/todos/** → CRUD de tareas
- **/** → Verificar estado de la API
    """,
    version="1.0.0",
    contact={
        "name": "Diego Aguirre",
        "url": "https://github.com/tuusuario",
        "email": "tuemail@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Excepciones
app.add_exception_handler(StarletteHTTPException, handlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, handlers.validation_exception_handler)
app.add_exception_handler(IntegrityError, handlers.sqlalchemy_integrity_error_handler)
app.add_exception_handler(ValidationError, handlers.pydantic_validation_error_handler)

# Eventos
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Aplicación iniciada")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Aplicación detenida")

# Rutas
app.include_router(todos.router, tags=["Todos"])  # Tag para organizar docs

@app.get("/", tags=["Health Check"])
def read_root():
    logger.info("📢 Endpoint raíz llamado")
    return {"message": f"{settings.project_name} funcionando 🚀"}
