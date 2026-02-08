"""
Script para crear datos de prueba en la base de datos
"""
import asyncio
import sys
sys.path.insert(0, '.')

from datetime import datetime, timedelta
from database import AsyncSessionLocal, init_db
from models import Lead


async def crear_datos_prueba():
    print("🔧 Creando datos de prueba...")
    
    await init_db()
    
    leads_ejemplo = [
        {
            "nombre": "María García López",
            "email": "maria.garcia@email.com",
            "telefono": "612345678",
            "tipo_seguro": "hogar",
            "mensaje": "Quiero asegurar mi piso en Las Rozas, 90m2",
            "localidad": "Las Rozas",
            "codigo_postal": "28231",
            "origen": "web",
            "estado": "nuevo"
        },
        {
            "nombre": "Carlos Rodríguez Martín",
            "email": "carlos.rm@gmail.com",
            "telefono": "634567890",
            "tipo_seguro": "auto",
            "mensaje": "Seguro para Seat León 2022",
            "localidad": "Majadahonda",
            "codigo_postal": "28220",
            "origen": "comparador",
            "estado": "contactado"
        },
        {
            "nombre": "Ana Fernández Ruiz",
            "email": "ana.fernandez@outlook.es",
            "telefono": "656789012",
            "tipo_seguro": "vida",
            "mensaje": "Interesada en seguro de vida, tengo 35 años",
            "localidad": "Madrid",
            "codigo_postal": "28001",
            "origen": "web",
            "estado": "nuevo"
        },
        {
            "nombre": "Pedro Sánchez Gil",
            "email": "pedro.sg@email.com",
            "telefono": "678901234",
            "tipo_seguro": "decesos",
            "mensaje": "Quiero información sobre seguros de decesos para familia",
            "localidad": "Los Molinos",
            "codigo_postal": "28460",
            "origen": "formulario_contacto",
            "estado": "cerrado_ganado"
        },
        {
            "nombre": "Laura Martínez López",
            "email": "laura.ml@gmail.com",
            "telefono": "690123456",
            "tipo_seguro": "salud",
            "mensaje": "Busco seguro de salud sin copago",
            "localidad": "Collado Villalba",
            "codigo_postal": "28400",
            "origen": "comparador",
            "estado": "nuevo"
        }
    ]
    
    async with AsyncSessionLocal() as db:
        for i, lead_data in enumerate(leads_ejemplo):
            # Crear fechas escalonadas
            fecha = datetime.utcnow() - timedelta(days=i, hours=i*2)
            
            lead = Lead(
                **lead_data,
                created_at=fecha,
                updated_at=fecha
            )
            db.add(lead)
        
        await db.commit()
        print(f"✅ Creados {len(leads_ejemplo)} leads de ejemplo")
    
    print("🎉 Datos de prueba creados correctamente")


if __name__ == "__main__":
    asyncio.run(crear_datos_prueba())
