"""
Script de prueba para verificar todas las configuraciones
"""
import asyncio
import sys
sys.path.insert(0, '.')

from config import settings


async def verificar_configuraciones():
    print("=" * 50)
    print("🔍 VERIFICACIÓN DE CONFIGURACIONES - SegurosPy")
    print("=" * 50)
    print()
    
    resultados = {
        "ok": [],
        "warning": [],
        "error": []
    }
    
    # 1. Verificar OpenAI
    print("1️⃣  OpenAI API Key:")
    if settings.openai_api_key and settings.openai_api_key.startswith("sk-"):
        print(f"   ✅ Configurada ({settings.openai_api_key[:10]}...)")
        resultados["ok"].append("OpenAI")
        
        # Probar conexión
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hola"}],
                max_tokens=10
            )
            print("   ✅ Conexión exitosa con OpenAI")
        except Exception as e:
            print(f"   ⚠️ Error de conexión: {e}")
            resultados["warning"].append("OpenAI conexión")
    else:
        print("   ⚠️ No configurada (usará respuestas predefinidas)")
        resultados["warning"].append("OpenAI")
    print()
    
    # 2. Verificar Telegram
    print("2️⃣  Telegram:")
    if settings.telegram_bot_token and settings.telegram_chat_id:
        print(f"   ✅ Bot Token configurado")
        print(f"   ✅ Chat ID: {settings.telegram_chat_id}")
        resultados["ok"].append("Telegram")
        
        # Probar envío
        try:
            from services.telegram_service import telegram_service
            exito = await telegram_service.enviar_mensaje("🧪 Test de configuración SegurosPy")
            if exito:
                print("   ✅ Mensaje de prueba enviado")
            else:
                print("   ⚠️ No se pudo enviar el mensaje")
                resultados["warning"].append("Telegram envío")
        except Exception as e:
            print(f"   ⚠️ Error: {e}")
            resultados["warning"].append("Telegram envío")
    else:
        print("   ⚠️ No configurado (notificaciones deshabilitadas)")
        resultados["warning"].append("Telegram")
    print()
    
    # 3. Verificar Email
    print("3️⃣  Email (SMTP):")
    if settings.smtp_user and settings.smtp_password:
        print(f"   ✅ Usuario: {settings.smtp_user}")
        print(f"   ✅ Servidor: {settings.smtp_host}:{settings.smtp_port}")
        resultados["ok"].append("Email")
        
        # Probar conexión SMTP
        try:
            import aiosmtplib
            smtp = aiosmtplib.SMTP(
                hostname=settings.smtp_host,
                port=settings.smtp_port,
                use_tls=False,
                start_tls=True
            )
            await smtp.connect()
            await smtp.login(settings.smtp_user, settings.smtp_password)
            await smtp.quit()
            print("   ✅ Conexión SMTP exitosa")
        except Exception as e:
            print(f"   ⚠️ Error SMTP: {e}")
            resultados["warning"].append("Email conexión")
    else:
        print("   ⚠️ No configurado (emails deshabilitados)")
        resultados["warning"].append("Email")
    print()
    
    # 4. Verificar Base de Datos
    print("4️⃣  Base de Datos:")
    try:
        from database import engine, init_db
        await init_db()
        print(f"   ✅ Conectada: {settings.database_url}")
        resultados["ok"].append("Database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados["error"].append("Database")
    print()
    
    # Resumen
    print("=" * 50)
    print("📊 RESUMEN")
    print("=" * 50)
    print(f"   ✅ Configurados: {len(resultados['ok'])}")
    print(f"   ⚠️ Advertencias: {len(resultados['warning'])}")
    print(f"   ❌ Errores: {len(resultados['error'])}")
    print()
    
    if resultados["error"]:
        print("❌ Hay errores que deben corregirse")
        return False
    elif len(resultados["ok"]) >= 2:
        print("✅ Sistema listo para producción")
        return True
    else:
        print("⚠️ Sistema funcionando en modo básico")
        return True


if __name__ == "__main__":
    asyncio.run(verificar_configuraciones())
