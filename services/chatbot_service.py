"""
Servicio de Chatbot IA - Equivalente al chat widget con OpenAI
"""
from openai import AsyncOpenAI
from config import settings
from typing import List, Dict, Optional
import logging
import uuid

logger = logging.getLogger(__name__)


# Prompt del sistema para el chatbot
SYSTEM_PROMPT = """Eres el asistente virtual de SegurosPy, una correduría de seguros en Madrid especializada en:
- Seguros de Hogar
- Seguros de Auto/Coche
- Seguros de Vida
- Seguros de Decesos
- Seguros de Salud
- Seguros para Mascotas
- Seguros para Autónomos

Tu objetivo es:
1. Responder preguntas frecuentes sobre seguros de forma clara y concisa
2. Ayudar a los usuarios a elegir el tipo de seguro que necesitan
3. Recopilar información básica para que un agente les contacte
4. Ser amable, profesional y cercano

Información de contacto:
- Teléfono/WhatsApp: 661 854 126
- Email: info@segurospy.com
- Horario: Lunes a Viernes 10:00-19:00
- Zona: Madrid, Las Rozas, Majadahonda, Los Molinos y Sierra de Madrid

Reglas:
- Nunca inventes precios específicos, di que un agente personalizará la cotización
- Si preguntan algo que no sabes, sugiere que contacten directamente
- Mantén respuestas cortas (máximo 3-4 frases)
- Usa emojis ocasionalmente para ser más cercano
- Siempre ofrece la opción de hablar con un agente humano
"""


class ChatbotService:
    """Servicio de chatbot con OpenAI"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.conversaciones: Dict[str, List[Dict]] = {}
    
    def _generar_session_id(self) -> str:
        """Genera un ID único de sesión"""
        return str(uuid.uuid4())
    
    def _get_historial(self, session_id: str) -> List[Dict]:
        """Obtiene el historial de una conversación"""
        if session_id not in self.conversaciones:
            self.conversaciones[session_id] = []
        return self.conversaciones[session_id]
    
    async def responder(
        self,
        mensaje: str,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Genera una respuesta del chatbot
        
        Args:
            mensaje: Mensaje del usuario
            session_id: ID de sesión para mantener contexto
        
        Returns:
            Dict con respuesta, session_id y sugerencias
        """
        # Generar session_id si no existe
        if not session_id:
            session_id = self._generar_session_id()
        
        # Si no hay API key, usar respuestas predefinidas
        if not self.client:
            return self._respuesta_fallback(mensaje, session_id)
        
        try:
            # Obtener historial
            historial = self._get_historial(session_id)
            
            # Construir mensajes
            mensajes = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            
            # Añadir historial (últimos 10 mensajes)
            mensajes.extend(historial[-10:])
            
            # Añadir mensaje actual
            mensajes.append({"role": "user", "content": mensaje})
            
            # Llamar a OpenAI
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=mensajes,
                max_tokens=300,
                temperature=0.7
            )
            
            respuesta = response.choices[0].message.content
            
            # Guardar en historial
            historial.append({"role": "user", "content": mensaje})
            historial.append({"role": "assistant", "content": respuesta})
            
            # Generar sugerencias
            sugerencias = self._generar_sugerencias(mensaje, respuesta)
            
            return {
                "respuesta": respuesta,
                "session_id": session_id,
                "sugerencias": sugerencias
            }
            
        except Exception as e:
            logger.error(f"Error en chatbot: {e}")
            return self._respuesta_fallback(mensaje, session_id)
    
    def _respuesta_fallback(self, mensaje: str, session_id: str) -> Dict:
        """Respuestas predefinidas cuando no hay API"""
        mensaje_lower = mensaje.lower()
        
        if any(p in mensaje_lower for p in ["precio", "coste", "cuanto", "cuánto"]):
            respuesta = "💰 El precio depende de varios factores. Un asesor te preparará una cotización personalizada gratuita. ¿Quieres que te llamemos? Déjanos tu teléfono."
        elif any(p in mensaje_lower for p in ["hogar", "casa", "vivienda", "piso"]):
            respuesta = "🏠 ¡El seguro de hogar es fundamental! Cubrimos daños por agua, incendio, robo y mucho más. ¿Te gustaría que un asesor te explique las opciones?"
        elif any(p in mensaje_lower for p in ["coche", "auto", "vehiculo", "vehículo"]):
            respuesta = "🚗 Comparamos más de 20 aseguradoras para encontrarte el mejor precio en seguro de coche. ¿Tienes el vehículo ya o es nuevo?"
        elif any(p in mensaje_lower for p in ["vida"]):
            respuesta = "💚 El seguro de vida protege a tu familia económicamente. Podemos encontrar opciones desde 10€/mes. ¿Quieres más información?"
        elif any(p in mensaje_lower for p in ["decesos", "funeral"]):
            respuesta = "🕊️ El seguro de decesos cubre todos los gastos y gestiones. Es muy económico y da tranquilidad a la familia. ¿Te informamos?"
        elif any(p in mensaje_lower for p in ["salud", "médico", "medico"]):
            respuesta = "🏥 Con el seguro de salud tendrás acceso a los mejores especialistas sin esperas. ¿Buscas cobertura individual o familiar?"
        elif any(p in mensaje_lower for p in ["mascota", "perro", "gato"]):
            respuesta = "🐾 ¡Protege a tu peludo! Cubrimos veterinario, responsabilidad civil y más. ¿Qué tipo de mascota tienes?"
        elif any(p in mensaje_lower for p in ["hola", "buenos", "buenas"]):
            respuesta = "👋 ¡Hola! Soy el asistente virtual de SegurosPy. ¿En qué puedo ayudarte? Puedo informarte sobre seguros de hogar, auto, vida, salud y más."
        elif any(p in mensaje_lower for p in ["contacto", "llamar", "teléfono", "telefono", "whatsapp"]):
            respuesta = "📞 Puedes contactarnos en:\n• Teléfono/WhatsApp: 661 854 126\n• Email: info@segurospy.com\n• Horario: L-V 10:00-19:00"
        else:
            respuesta = "Gracias por tu mensaje. Para darte la mejor información, ¿podrías indicarme qué tipo de seguro te interesa? (hogar, coche, vida, salud, decesos, mascotas)"
        
        return {
            "respuesta": respuesta,
            "session_id": session_id,
            "sugerencias": ["Seguro de Hogar", "Seguro de Coche", "Contactar con agente"]
        }
    
    def _generar_sugerencias(self, mensaje: str, respuesta: str) -> List[str]:
        """Genera sugerencias de preguntas siguientes"""
        return [
            "¿Cuánto cuesta?",
            "Quiero que me llamen",
            "Más información"
        ]


# Instancia singleton
chatbot_service = ChatbotService()
