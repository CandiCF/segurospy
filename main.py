"""
SegurosPy - Aplicación Principal
Equivalente a todo el sistema de segurospy.com pero en Python

Ejecutar con: uvicorn main:app --reload
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import settings
from database import init_db
from routers import leads_router, chat_router, pages_router
from tasks import iniciar_tareas, detener_tareas

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Eventos de ciclo de vida de la aplicación
    - Al iniciar: crear BD y arrancar tareas
    - Al cerrar: detener tareas
    """
    logger.info("🚀 Iniciando SegurosPy...")
    
    # Inicializar base de datos
    await init_db()
    logger.info("✅ Base de datos inicializada")
    
    # Iniciar tareas programadas (equivalente a n8n)
    iniciar_tareas()
    logger.info("✅ Tareas programadas activas")
    
    yield
    
    # Cleanup
    detener_tareas()
    logger.info("👋 SegurosPy detenido")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="""
    ## 🏠 SegurosPy - Sistema de Gestión para Agentes de Seguros
    
    API completa para:
    - 📝 Gestión de leads desde formularios web
    - 🤖 Chatbot IA para atención al cliente
    - 📧 Notificaciones por email y Telegram
    - ⏰ Tareas automatizadas (equivalente a n8n)
    - 📊 Dashboard y CRM básico
    
    ### Tecnologías:
    - **Backend**: FastAPI + Python 3.11+
    - **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
    - **Templates**: Jinja2
    - **Tareas**: APScheduler
    - **IA**: OpenAI GPT-4
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,  # Swagger solo en desarrollo
    redoc_url="/redoc" if settings.debug else None
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["https://segurospy.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar routers
app.include_router(pages_router)      # Páginas HTML
app.include_router(leads_router)      # API de leads
app.include_router(chat_router)       # API del chatbot


# =============================================
# ENDPOINT DE SALUD
# =============================================

@app.get("/health", tags=["Sistema"])
async def health_check():
    """
    Verificar que la aplicación está funcionando
    Útil para monitoreo y load balancers
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.app_env
    }


@app.get("/api/stats", tags=["Sistema"])
async def get_stats():
    """
    Estadísticas básicas del sistema
    """
    from sqlalchemy import select, func
    from database import AsyncSessionLocal
    from models import Lead
    from datetime import datetime, timedelta
    
    async with AsyncSessionLocal() as db:
        # Total leads
        total_result = await db.execute(select(func.count()).select_from(Lead))
        total_leads = total_result.scalar()
        
        # Leads hoy
        hoy = datetime.utcnow().date()
        inicio_dia = datetime.combine(hoy, datetime.min.time())
        hoy_result = await db.execute(
            select(func.count()).select_from(Lead).where(Lead.created_at >= inicio_dia)
        )
        leads_hoy = hoy_result.scalar()
        
        # Leads esta semana
        inicio_semana = datetime.utcnow() - timedelta(days=7)
        semana_result = await db.execute(
            select(func.count()).select_from(Lead).where(Lead.created_at >= inicio_semana)
        )
        leads_semana = semana_result.scalar()
        
        return {
            "total_leads": total_leads,
            "leads_hoy": leads_hoy,
            "leads_semana": leads_semana
        }


# =============================================
# PUNTO DE ENTRADA
# =============================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
