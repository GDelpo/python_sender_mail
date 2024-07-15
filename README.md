# API para gestión de correos electrónicos

Este proyecto es una API para la gestión de envíos de correos electrónicos y autenticación de usuarios utilizando JWT, construida con FastAPI.

## Requisitos

- Python 3.10+
- Servidor SMTP (por ejemplo, Gmail)


## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/GDelpo/python_sender_mail.git
cd python_sender_mail
```

2. Crea y activa un entorno virtual:

```bash
python -m venv env
source env/bin/activate  # En Windows: .\env\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Asegúrate de tener un archivo `.env` con todas las configuraciones necesarias. Revisar el `.env.example` para más información.

## Estructura del Proyecto

```plaintext
.
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── crud.py
│   ├── db_manager.py
│   ├── main.py
│   ├── mailer.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── email.py
│   │   ├── user.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── emails.py
│   │   ├── users.py
│   ├── scheduler.py
│   ├── security.py
│   ├── utils.py
├── .env
├── requirements.txt
├── README.md
```

## Uso

### Ejecutar la Aplicación

Para ejecutar la aplicación, utilizar el run.py o el siguiente comando:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Documentación de la API

La documentación de la API estará disponible en:

- Swagger UI: [http://127.0.0.1:8000/documentation](http://127.0.0.1:8000/documentation)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoints

#### Usuarios

- **Crear usuario**: `POST /users/`
- **Generar token**: `POST /users/token`

#### Correos Electrónicos

- **Enviar correo electrónico**: `POST /emails/send-email`
- **Consultar estado de correo**: `GET /emails/{email_id}`