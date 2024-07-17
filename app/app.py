from contextlib import asynccontextmanager
from fastapi import FastAPI

from .db_manager import create_db_and_tables
from .scheduler import start_scheduler, shutdown_scheduler
from .routers import email, users 

description = """
API para la gestión de envíos de correos electrónicos y autenticación de usuarios con JWT.

## Permisos para los servicios(**Servicios**)

* **Crear servicio** (_implementado_).
* **Generar tokens de acceso para servicio** (_implementado_).

## Correos Electrónicos

* **Enviar correos electrónicos** (_implementado_).
* **Consultar estado de correos electrónicos** (_implementado_).
"""

tags_metadata = [
    {
        "name": "users",
        "description": "Operaciones con usuarios. La lógica de **login** y **registro** está aquí.",
    },
    {
        "name": "emails",
        "description": "Gestionar envíos de correos electrónicos. Operaciones para enviar y consultar correos electrónicos.",
    },
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización antes de que la aplicación comience a recibir solicitudes
    create_db_and_tables()
    #start_scheduler()
    yield
    # Limpieza después de que la aplicación deje de recibir solicitudes
    #shutdown_scheduler()

app = FastAPI( lifespan=lifespan, 
    title="Gestión de Correos Electrónicos",
    description=description,
    version="1.0.0",
    contact={
        "name": "Guido Delponte - Sistemas",
        "email": "guido.delponte@nobleseguros.com",
    },
    openapi_tags=tags_metadata
)
#root_path="/api/v1",
app.include_router(email.router)
app.include_router(users.router)


