"""
Router del Chatbot IA
"""
from fastapi import APIRouter
from schemas import ChatMessage, ChatResponse
from services import chatbot_service

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])


@router.post("/", response_model=ChatResponse)
async def chat(mensaje: ChatMessage):
    """
    Endpoint del chatbot IA
    Recibe un mensaje y devuelve la respuesta del asistente
    """
    resultado = await chatbot_service.responder(
        mensaje=mensaje.mensaje,
        session_id=mensaje.session_id
    )
    
    return ChatResponse(
        respuesta=resultado["respuesta"],
        session_id=resultado["session_id"],
        sugerencias=resultado.get("sugerencias")
    )
