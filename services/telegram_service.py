"""
Servicio de Telegram - Equivalente al nodo de Telegram en n8n
"""
import httpx
from config import settings
import logging

logger = logging.getLogger(__name__)


class TelegramService:
    """Servicio para enviar notificaciones a Telegram"""
    
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def enviar_mensaje(self, mensaje: str, parse_mode: str = "HTML") -> bool:
        """
        Envía un mensaje a Telegram
        
        Args:
            mensaje: Texto del mensaje (puede incluir HTML)
            parse_mode: Formato del mensaje (HTML o Markdown)
        
        Returns:
            bool: True si se envió correctamente
        """
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram no configurado")
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": mensaje,
                        "parse_mode": parse_mode
                    }
                )
                
                if response.status_code == 200:
                    logger.info("Mensaje de Telegram enviado")
                    return True
                else:
                    logger.error(f"Error Telegram: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error enviando a Telegram: {e}")
            return False
    
    async def notificar_nuevo_lead(self, lead_data: dict) -> bool:
        """
        Notifica un nuevo lead por Telegram
        """
        mensaje = f"""
🚨 <b>NUEVO LEAD</b> 🚨

👤 <b>Nombre:</b> {lead_data['nombre']}
📧 <b>Email:</b> {lead_data['email']}
📞 <b>Teléfono:</b> {lead_data['telefono']}
🏷️ <b>Seguro:</b> {lead_data['tipo_seguro'].upper()}
📍 <b>Origen:</b> {lead_data.get('origen', 'web')}

💬 <b>Mensaje:</b>
{lead_data.get('mensaje', 'Sin mensaje')}

⏰ {lead_data.get('created_at', 'Ahora')}
        """
        
        return await self.enviar_mensaje(mensaje.strip())
    
    async def notificar_error(self, error: str, contexto: str = "") -> bool:
        """
        Notifica un error al administrador
        """
        mensaje = f"""
⚠️ <b>ERROR EN SEGUROSPY</b>

🔴 <b>Error:</b> {error}
📋 <b>Contexto:</b> {contexto}
        """
        
        return await self.enviar_mensaje(mensaje.strip())


# Instancia singleton
telegram_service = TelegramService()
