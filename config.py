"""
Configuración centralizada de la aplicación SegurosPy
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic"""
    
    # App
    app_name: str = "Candi Seguros"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "cambiar-en-produccion"
    
    # Base de datos
    database_url: str = "sqlite+aiosqlite:///./segurospy.db"
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "candi@candiseguros.com"
    notification_email: str = "candi@candiseguros.com"
    
    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    # OpenAI
    openai_api_key: str = ""
    
    # Empresa
    company_name: str = "Candi Seguros"
    company_phone: str = "661854126"
    company_email: str = "candi@candiseguros.com"
    google_review_url: str = "https://g.page/r/candiseguros/review"
    whatsapp_phone: str = "34661854126"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignorar variables extra en .env


@lru_cache()
def get_settings() -> Settings:
    """Singleton para obtener la configuración"""
    return Settings()


# Instancia global
settings = get_settings()
