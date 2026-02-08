"""
Tareas Programadas - Equivalente a los Workflows de n8n
Usa APScheduler para ejecutar tareas en segundo plano
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from database import AsyncSessionLocal
from models import Lead, SolicitudResena
from services import email_service, telegram_service

logger = logging.getLogger(__name__)

# Scheduler global
scheduler = AsyncIOScheduler()


# =============================================
# TAREA 1: Informe diario de leads
# Equivalente a: n8n_workflow_informe_semanal.json
# =============================================

async def tarea_informe_diario():
    """
    Envía un resumen diario de los leads recibidos
    Se ejecuta cada día a las 20:00
    """
    logger.info("Ejecutando tarea: Informe diario de leads")
    
    async with AsyncSessionLocal() as db:
        # Leads de hoy
        hoy = datetime.utcnow().date()
        inicio_dia = datetime.combine(hoy, datetime.min.time())
        
        query = select(Lead).where(Lead.created_at >= inicio_dia)
        result = await db.execute(query)
        leads_hoy = result.scalars().all()
        
        # Contar por tipo
        por_tipo = {}
        for lead in leads_hoy:
            tipo = lead.tipo_seguro
            por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        
        # Preparar mensaje
        mensaje = f"""
📊 <b>INFORME DIARIO - {hoy.strftime('%d/%m/%Y')}</b>

📈 <b>Leads recibidos:</b> {len(leads_hoy)}

📋 <b>Por tipo de seguro:</b>
"""
        for tipo, cantidad in por_tipo.items():
            mensaje += f"  • {tipo.capitalize()}: {cantidad}\n"
        
        if not leads_hoy:
            mensaje += "\n😢 No se recibieron leads hoy."
        
        mensaje += f"\n⏰ Generado: {datetime.now().strftime('%H:%M')}"
        
        # Enviar por Telegram
        await telegram_service.enviar_mensaje(mensaje)
        
        logger.info(f"Informe diario enviado: {len(leads_hoy)} leads")


# =============================================
# TAREA 2: Solicitar reseñas a clientes
# Equivalente a: n8n_workflow_solicitar_resenas.json
# =============================================

async def tarea_solicitar_resenas():
    """
    Envía emails solicitando reseñas a clientes satisfechos
    Se ejecuta cada día a las 10:00
    Envía a leads cerrados hace 7 días
    """
    logger.info("Ejecutando tarea: Solicitar reseñas")
    
    async with AsyncSessionLocal() as db:
        # Leads cerrados ganados hace 7 días
        hace_7_dias = datetime.utcnow() - timedelta(days=7)
        hace_8_dias = datetime.utcnow() - timedelta(days=8)
        
        query = select(Lead).where(
            Lead.estado == "cerrado_ganado",
            Lead.updated_at >= hace_8_dias,
            Lead.updated_at <= hace_7_dias
        )
        result = await db.execute(query)
        leads = result.scalars().all()
        
        enviados = 0
        for lead in leads:
            # Verificar si ya se envió
            check_query = select(SolicitudResena).where(
                SolicitudResena.lead_id == lead.id
            )
            check_result = await db.execute(check_query)
            if check_result.scalar_one_or_none():
                continue
            
            # Enviar email de solicitud
            exito = await email_service.enviar_email(
                destinatario=lead.email,
                asunto="¿Qué tal tu experiencia con Candi Seguros? ⭐",
                contenido_html=f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>Hola {lead.nombre},</h2>
                    <p>Esperamos que estés disfrutando de tu nuevo seguro. 🎉</p>
                    <p>Tu opinión es muy importante para nosotros. ¿Podrías dedicarnos 
                    1 minuto para dejarnos una reseña en Google?</p>
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="https://g.page/r/CXxXxXxXx/review" 
                           style="background: #6366f1; color: white; padding: 15px 30px; 
                                  text-decoration: none; border-radius: 8px;">
                            ⭐ Dejar Reseña
                        </a>
                    </p>
                    <p>¡Gracias por confiar en nosotros!</p>
                    <p><strong>El equipo de Candi Seguros</strong></p>
                </body>
                </html>
                """
            )
            
            if exito:
                # Registrar envío
                solicitud = SolicitudResena(
                    lead_id=lead.id,
                    email_enviado=True,
                    fecha_envio=datetime.utcnow()
                )
                db.add(solicitud)
                enviados += 1
        
        await db.commit()
        logger.info(f"Solicitudes de reseña enviadas: {enviados}")


# =============================================
# TAREA 3: Recordatorio de leads sin contactar
# Equivalente a: Alerta de leads pendientes
# =============================================

async def tarea_leads_pendientes():
    """
    Alerta sobre leads que llevan más de 24h sin contactar
    Se ejecuta cada 4 horas
    """
    logger.info("Ejecutando tarea: Leads pendientes")
    
    async with AsyncSessionLocal() as db:
        hace_24h = datetime.utcnow() - timedelta(hours=24)
        
        query = select(Lead).where(
            Lead.estado == "nuevo",
            Lead.created_at <= hace_24h
        )
        result = await db.execute(query)
        leads_pendientes = result.scalars().all()
        
        if leads_pendientes:
            mensaje = f"""
⚠️ <b>ALERTA: {len(leads_pendientes)} LEADS SIN CONTACTAR</b>

Los siguientes leads llevan más de 24 horas sin respuesta:

"""
            for lead in leads_pendientes[:10]:  # Máximo 10
                horas = int((datetime.utcnow() - lead.created_at).total_seconds() / 3600)
                mensaje += f"• <b>{lead.nombre}</b> ({lead.tipo_seguro}) - {horas}h\n"
            
            if len(leads_pendientes) > 10:
                mensaje += f"\n... y {len(leads_pendientes) - 10} más"
            
            await telegram_service.enviar_mensaje(mensaje)
            
        logger.info(f"Leads pendientes: {len(leads_pendientes)}")


# =============================================
# TAREA 4: Limpieza de conversaciones antiguas
# =============================================

async def tarea_limpieza():
    """
    Limpia conversaciones del chatbot antiguas (más de 7 días)
    Se ejecuta cada domingo a las 03:00
    """
    logger.info("Ejecutando tarea: Limpieza de datos")
    
    from models import Conversacion
    from sqlalchemy import delete
    
    async with AsyncSessionLocal() as db:
        hace_7_dias = datetime.utcnow() - timedelta(days=7)
        
        stmt = delete(Conversacion).where(Conversacion.created_at < hace_7_dias)
        result = await db.execute(stmt)
        await db.commit()
        
        logger.info(f"Conversaciones eliminadas: {result.rowcount}")


# =============================================
# CONFIGURACIÓN DEL SCHEDULER
# =============================================

def iniciar_tareas():
    """Configura e inicia todas las tareas programadas"""
    
    # Informe diario a las 20:00
    scheduler.add_job(
        tarea_informe_diario,
        CronTrigger(hour=20, minute=0),
        id="informe_diario",
        name="Informe diario de leads"
    )
    
    # Solicitar reseñas a las 10:00
    scheduler.add_job(
        tarea_solicitar_resenas,
        CronTrigger(hour=10, minute=0),
        id="solicitar_resenas",
        name="Solicitar reseñas"
    )
    
    # Leads pendientes cada 4 horas
    scheduler.add_job(
        tarea_leads_pendientes,
        CronTrigger(hour="*/4"),
        id="leads_pendientes",
        name="Alertar leads pendientes"
    )
    
    # Limpieza domingos a las 03:00
    scheduler.add_job(
        tarea_limpieza,
        CronTrigger(day_of_week="sun", hour=3, minute=0),
        id="limpieza",
        name="Limpieza semanal"
    )
    
    # Iniciar scheduler
    scheduler.start()
    logger.info("Tareas programadas iniciadas")


def detener_tareas():
    """Detiene el scheduler"""
    scheduler.shutdown()
    logger.info("Tareas programadas detenidas")
