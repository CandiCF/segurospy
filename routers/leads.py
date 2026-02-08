"""
Router de Leads - API para gestión de leads
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import datetime

from database import get_db
from models import Lead
from schemas import (
    LeadCreate, LeadUpdate, LeadResponse, 
    LeadListResponse, ContactoForm, ContactoResponse,
    ComparadorForm, ComparadorResponse
)
from services import email_service, telegram_service

router = APIRouter(prefix="/api/leads", tags=["Leads"])


@router.post("/", response_model=LeadResponse)
async def crear_lead(
    lead_data: LeadCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Crear un nuevo lead desde el formulario
    Equivalente al webhook de n8n que recibe el formulario
    """
    # Crear el lead
    nuevo_lead = Lead(
        nombre=lead_data.nombre,
        email=lead_data.email,
        telefono=lead_data.telefono,
        tipo_seguro=lead_data.tipo_seguro.value,
        mensaje=lead_data.mensaje,
        localidad=lead_data.localidad,
        codigo_postal=lead_data.codigo_postal,
        origen=lead_data.origen,
        landing_page=lead_data.landing_page,
        utm_source=lead_data.utm_source,
        utm_medium=lead_data.utm_medium,
        utm_campaign=lead_data.utm_campaign,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    
    db.add(nuevo_lead)
    await db.commit()
    await db.refresh(nuevo_lead)
    
    # Preparar datos para notificaciones
    lead_dict = {
        "nombre": nuevo_lead.nombre,
        "email": nuevo_lead.email,
        "telefono": nuevo_lead.telefono,
        "tipo_seguro": nuevo_lead.tipo_seguro,
        "mensaje": nuevo_lead.mensaje,
        "origen": nuevo_lead.origen,
        "created_at": nuevo_lead.created_at.strftime("%d/%m/%Y %H:%M")
    }
    
    # Enviar notificaciones (en background idealmente)
    await email_service.notificar_nuevo_lead(lead_dict)
    await telegram_service.notificar_nuevo_lead(lead_dict)
    await email_service.enviar_confirmacion_cliente(lead_dict)
    
    return nuevo_lead


@router.post("/contacto", response_model=ContactoResponse)
async def formulario_contacto(
    form: ContactoForm,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Procesar formulario de contacto simple
    """
    if not form.acepta_privacidad:
        raise HTTPException(status_code=400, detail="Debe aceptar la política de privacidad")
    
    # Crear lead desde contacto
    nuevo_lead = Lead(
        nombre=form.nombre,
        email=form.email,
        telefono=form.telefono,
        tipo_seguro="consulta",
        mensaje=f"[{form.asunto}] {form.mensaje}",
        origen="formulario_contacto",
        ip_address=request.client.host if request.client else None
    )
    
    db.add(nuevo_lead)
    await db.commit()
    await db.refresh(nuevo_lead)
    
    # Notificar
    lead_dict = {
        "nombre": form.nombre,
        "email": form.email,
        "telefono": form.telefono,
        "tipo_seguro": "Consulta General",
        "mensaje": form.mensaje,
        "origen": "formulario_contacto"
    }
    
    await email_service.notificar_nuevo_lead(lead_dict)
    await telegram_service.notificar_nuevo_lead(lead_dict)
    
    return ContactoResponse(
        success=True,
        mensaje="¡Gracias! Hemos recibido tu mensaje. Te contactaremos pronto.",
        lead_id=nuevo_lead.id
    )


@router.post("/comparador", response_model=ComparadorResponse)
async def formulario_comparador(
    form: ComparadorForm,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Procesar formulario del comparador de seguros
    """
    # Construir mensaje con datos adicionales
    detalles = []
    if form.codigo_postal:
        detalles.append(f"CP: {form.codigo_postal}")
    if form.fecha_nacimiento:
        detalles.append(f"Nacimiento: {form.fecha_nacimiento}")
    if form.tipo_vivienda:
        detalles.append(f"Vivienda: {form.tipo_vivienda}")
    if form.metros_cuadrados:
        detalles.append(f"M²: {form.metros_cuadrados}")
    if form.marca_vehiculo:
        detalles.append(f"Vehículo: {form.marca_vehiculo} {form.modelo_vehiculo} ({form.ano_vehiculo})")
    
    mensaje = " | ".join(detalles) if detalles else None
    
    # Crear lead
    nuevo_lead = Lead(
        nombre=form.nombre,
        email=form.email,
        telefono=form.telefono,
        tipo_seguro=form.tipo_seguro.value,
        mensaje=mensaje,
        codigo_postal=form.codigo_postal,
        origen="comparador",
        ip_address=request.client.host if request.client else None
    )
    
    db.add(nuevo_lead)
    await db.commit()
    await db.refresh(nuevo_lead)
    
    # Notificar
    lead_dict = {
        "nombre": form.nombre,
        "email": form.email,
        "telefono": form.telefono,
        "tipo_seguro": form.tipo_seguro.value,
        "mensaje": mensaje,
        "origen": "comparador"
    }
    
    await email_service.notificar_nuevo_lead(lead_dict)
    await telegram_service.notificar_nuevo_lead(lead_dict)
    await email_service.enviar_confirmacion_cliente(lead_dict)
    
    return ComparadorResponse(
        success=True,
        mensaje="¡Solicitud recibida! Un asesor te contactará en menos de 24 horas.",
        lead_id=nuevo_lead.id
    )


@router.get("/", response_model=LeadListResponse)
async def listar_leads(
    pagina: int = 1,
    por_pagina: int = 20,
    estado: Optional[str] = None,
    tipo_seguro: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Listar leads con paginación y filtros (para panel admin/CRM)
    """
    query = select(Lead)
    
    # Filtros
    if estado:
        query = query.where(Lead.estado == estado)
    if tipo_seguro:
        query = query.where(Lead.tipo_seguro == tipo_seguro)
    
    # Ordenar por más reciente
    query = query.order_by(Lead.created_at.desc())
    
    # Contar total
    count_query = select(func.count()).select_from(Lead)
    if estado:
        count_query = count_query.where(Lead.estado == estado)
    if tipo_seguro:
        count_query = count_query.where(Lead.tipo_seguro == tipo_seguro)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Paginar
    offset = (pagina - 1) * por_pagina
    query = query.offset(offset).limit(por_pagina)
    
    result = await db.execute(query)
    leads = result.scalars().all()
    
    return LeadListResponse(
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        leads=leads
    )


@router.get("/{lead_id}", response_model=LeadResponse)
async def obtener_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtener un lead por ID
    """
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    
    return lead


@router.patch("/{lead_id}", response_model=LeadResponse)
async def actualizar_lead(
    lead_id: int,
    update_data: LeadUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar estado de un lead (CRM)
    """
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    
    # Actualizar campos
    if update_data.estado:
        lead.estado = update_data.estado.value
        if update_data.estado.value == "contactado" and not lead.contacted_at:
            lead.contacted_at = datetime.utcnow()
    
    if update_data.asignado_a:
        lead.asignado_a = update_data.asignado_a
    
    if update_data.notas_internas:
        lead.notas_internas = update_data.notas_internas
    
    await db.commit()
    await db.refresh(lead)
    
    return lead
