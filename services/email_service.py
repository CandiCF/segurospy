"""
Servicio de Email - Equivalente al nodo de Gmail en n8n
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Servicio para envío de emails"""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.email_from = settings.email_from
    
    async def enviar_email(
        self,
        destinatario: str,
        asunto: str,
        contenido_html: str,
        contenido_texto: Optional[str] = None
    ) -> bool:
        """
        Envía un email
        
        Args:
            destinatario: Email del destinatario
            asunto: Asunto del email
            contenido_html: Contenido en HTML
            contenido_texto: Contenido en texto plano (opcional)
        
        Returns:
            bool: True si se envió correctamente
        """
        try:
            mensaje = MIMEMultipart("alternative")
            mensaje["From"] = self.email_from
            mensaje["To"] = destinatario
            mensaje["Subject"] = asunto
            
            # Versión texto plano
            if contenido_texto:
                parte_texto = MIMEText(contenido_texto, "plain", "utf-8")
                mensaje.attach(parte_texto)
            
            # Versión HTML
            parte_html = MIMEText(contenido_html, "html", "utf-8")
            mensaje.attach(parte_html)
            
            # Enviar
            await aiosmtplib.send(
                mensaje,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            
            logger.info(f"Email enviado a {destinatario}: {asunto}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email: {e}")
            return False
    
    async def notificar_nuevo_lead(self, lead_data: dict) -> bool:
        """
        Envía notificación de nuevo lead (equivalente al workflow de n8n)
        """
        asunto = f"🚨 Nuevo Lead: {lead_data['nombre']} - {lead_data['tipo_seguro']}"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #6366f1; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f8fafc; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #4b5563; }}
                .value {{ color: #1f2937; }}
                .cta {{ background: #10b981; color: white; padding: 15px 30px; 
                        text-decoration: none; display: inline-block; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 ¡Nuevo Lead!</h1>
                </div>
                <div class="content">
                    <div class="field">
                        <span class="label">Nombre:</span>
                        <span class="value">{lead_data['nombre']}</span>
                    </div>
                    <div class="field">
                        <span class="label">Email:</span>
                        <span class="value">{lead_data['email']}</span>
                    </div>
                    <div class="field">
                        <span class="label">Teléfono:</span>
                        <span class="value">{lead_data['telefono']}</span>
                    </div>
                    <div class="field">
                        <span class="label">Tipo de Seguro:</span>
                        <span class="value">{lead_data['tipo_seguro']}</span>
                    </div>
                    <div class="field">
                        <span class="label">Mensaje:</span>
                        <span class="value">{lead_data.get('mensaje', 'Sin mensaje')}</span>
                    </div>
                    <div class="field">
                        <span class="label">Origen:</span>
                        <span class="value">{lead_data.get('origen', 'web')}</span>
                    </div>
                    
                    <a href="tel:{lead_data['telefono']}" class="cta">
                        📞 Llamar Ahora
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.enviar_email(
            destinatario=self.smtp_user,  # Tu email
            asunto=asunto,
            contenido_html=html
        )
    
    async def enviar_confirmacion_cliente(self, lead_data: dict) -> bool:
        """
        Envía email de confirmación al cliente
        """
        asunto = "✅ Hemos recibido tu solicitud - SegurosPy"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); 
                          color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; background: #fff; }}
                .highlight {{ background: #f0f9ff; padding: 15px; border-left: 4px solid #6366f1; 
                             margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>¡Gracias, {lead_data['nombre']}!</h1>
                    <p>Hemos recibido tu solicitud</p>
                </div>
                <div class="content">
                    <p>Hola {lead_data['nombre']},</p>
                    
                    <p>Gracias por confiar en <strong>SegurosPy</strong>. Hemos recibido 
                    tu solicitud de información sobre <strong>seguro de {lead_data['tipo_seguro']}</strong>.</p>
                    
                    <div class="highlight">
                        <strong>⏰ ¿Qué pasa ahora?</strong><br>
                        Un asesor especializado te contactará en las próximas <strong>24 horas</strong> 
                        para ofrecerte las mejores opciones del mercado.
                    </div>
                    
                    <p>Si tienes alguna urgencia, puedes contactarnos directamente:</p>
                    <ul>
                        <li>📞 Teléfono: 661 854 126</li>
                        <li>💬 WhatsApp: 661 854 126</li>
                        <li>📧 Email: info@segurospy.com</li>
                    </ul>
                    
                    <p>¡Gracias por elegirnos!</p>
                    <p><strong>El equipo de SegurosPy</strong></p>
                </div>
                <div class="footer">
                    <p>SegurosPy - Tu agente de seguros de confianza en Madrid</p>
                    <p>Los Molinos, Madrid | segurospy.com</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.enviar_email(
            destinatario=lead_data['email'],
            asunto=asunto,
            contenido_html=html
        )


# Instancia singleton
email_service = EmailService()
