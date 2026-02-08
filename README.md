# 🐍 SegurosPy

**Sistema de Gestión Web para Corredurías de Seguros desarrollado en Python**

Este proyecto es la versión Python del sistema de SegurosPy, demostrando cómo implementar las mismas funcionalidades usando un stack de Python moderno.

---

## 📊 Comparación: HTML Estático vs Python

| Característica | HTML Estático (segurospy) | Python (segurosPy) |
|----------------|------------------------------|---------------------|
| **Tecnología Frontend** | HTML/CSS/JS puros | Jinja2 Templates |
| **Comparador** | React + Vite | Python + Jinja2 |
| **Backend** | No tiene (estático) | FastAPI |
| **Base de Datos** | Google Sheets (vía n8n) | SQLite/PostgreSQL |
| **Automatizaciones** | n8n workflows | APScheduler (Python) |
| **Chatbot IA** | Widget JS + webhook | Python + OpenAI |
| **Notificaciones** | n8n | Python (aiosmtplib, httpx) |
| **Hosting** | Cualquier hosting básico | Necesita servidor Python |
| **Complejidad** | Baja | Media-Alta |
| **Escalabilidad** | Limitada | Alta |

---

## 🚀 Inicio Rápido

### 1. Clonar e instalar dependencias

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus credenciales
notepad .env
```

### 3. Ejecutar la aplicación

```bash
# Modo desarrollo (con auto-reload)
uvicorn main:app --reload

# La aplicación estará en: http://localhost:8000
```

### 4. Ver la documentación de la API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Estructura del Proyecto

```
segurosPy/
├── main.py              # 🚀 Aplicación principal FastAPI
├── config.py            # ⚙️ Configuración centralizada
├── database.py          # 🗄️ Conexión a base de datos
├── models.py            # 📊 Modelos SQLAlchemy (Lead, Articulo, etc.)
├── schemas.py           # ✅ Validación Pydantic
├── requirements.txt     # 📦 Dependencias
├── .env.example         # 🔐 Variables de entorno (ejemplo)
│
├── routers/             # 🛣️ Endpoints de la API
│   ├── leads.py         # API de gestión de leads
│   ├── chat.py          # API del chatbot IA
│   └── pages.py         # Renderizado de páginas HTML
│
├── services/            # 🔧 Lógica de negocio
│   ├── email_service.py     # Envío de emails
│   ├── telegram_service.py  # Notificaciones Telegram
│   └── chatbot_service.py   # Chatbot con OpenAI
│
├── tasks/               # ⏰ Tareas programadas (equivalente a n8n)
│   └── scheduler.py     # APScheduler con tareas automáticas
│
├── templates/           # 🎨 Plantillas Jinja2
│   ├── base.html        # Layout principal
│   └── pages/           # Páginas individuales
│       ├── index.html
│       ├── comparador.html
│       └── ...
│
└── static/              # 📂 Archivos estáticos
    ├── css/
    ├── js/
    └── images/
```

---

## 🔌 API Endpoints

### Leads

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/leads/` | Crear nuevo lead |
| `POST` | `/api/leads/contacto` | Formulario de contacto |
| `POST` | `/api/leads/comparador` | Formulario del comparador |
| `GET` | `/api/leads/` | Listar leads (paginado) |
| `GET` | `/api/leads/{id}` | Obtener lead por ID |
| `PATCH` | `/api/leads/{id}` | Actualizar lead |

### Chatbot

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/chat/` | Enviar mensaje al chatbot |

### Sistema

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/health` | Estado de la aplicación |
| `GET` | `/api/stats` | Estadísticas de leads |

---

## ⏰ Tareas Programadas

Equivalentes a los workflows de n8n:

| Tarea | Frecuencia | Descripción |
|-------|------------|-------------|
| `tarea_informe_diario` | 20:00 cada día | Resumen de leads a Telegram |
| `tarea_solicitar_resenas` | 10:00 cada día | Email de reseña a clientes |
| `tarea_leads_pendientes` | Cada 4 horas | Alerta de leads sin contactar |
| `tarea_limpieza` | Domingos 03:00 | Limpiar datos antiguos |

---

## 🔐 Variables de Entorno

```env
# App
APP_NAME="SegurosPy"
DEBUG=true
SECRET_KEY=tu-clave-secreta

# Base de datos
DATABASE_URL=sqlite+aiosqlite:///./segurospy.db

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=contraseña-de-aplicacion

# Telegram
TELEGRAM_BOT_TOKEN=tu-bot-token
TELEGRAM_CHAT_ID=tu-chat-id

# OpenAI (para chatbot)
OPENAI_API_KEY=sk-tu-api-key

# WhatsApp
WHATSAPP_PHONE=34661854126
```

---

## 🌐 Despliegue en Producción

### Opción 1: VPS (DigitalOcean, Hetzner, etc.)

```bash
# Instalar dependencias del sistema
sudo apt update
sudo apt install python3.11 python3.11-venv nginx

# Crear usuario y directorio
sudo useradd -m segurospy
sudo mkdir -p /var/www/segurospy

# Configurar Gunicorn como servicio
sudo nano /etc/systemd/system/segurospy.service
```

```ini
[Unit]
Description=SegurosPy FastAPI
After=network.target

[Service]
User=segurospy
WorkingDirectory=/var/www/segurospy
ExecStart=/var/www/segurospy/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Opción 2: Railway / Render / Fly.io

Estas plataformas soportan despliegue automático desde GitHub.

### Opción 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🆚 ¿Cuándo usar cada versión?

### Usa HTML Estático (segurospy) cuando:
- ✅ Solo necesitas una web informativa
- ✅ No necesitas base de datos propia
- ✅ Quieres hosting muy barato
- ✅ No tienes conocimientos de Python

### Usa Python (segurosPy) cuando:
- ✅ Necesitas un CRM/Dashboard propio
- ✅ Quieres control total sobre los datos
- ✅ Necesitas lógica de negocio compleja
- ✅ Quieres escalar a múltiples usuarios/oficinas
- ✅ Necesitas integraciones personalizadas

---

## 📚 Recursos de Aprendizaje

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [APScheduler](https://apscheduler.readthedocs.io/)

---

## 📞 Soporte

- **Email**: info@segurospy.com
- **WhatsApp**: 661 854 126

---

## 📄 Licencia

Este proyecto es privado y de uso exclusivo para SegurosPy.

---

*Desarrollado con ❤️ y Python*
