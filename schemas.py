"""
Schemas Pydantic - Validación de datos de entrada/salida
Equivalente a la validación que hace React en el formulario
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ===========================================
# ENUMS
# ===========================================

class TipoSeguroEnum(str, Enum):
    hogar = "hogar"
    auto = "auto"
    vida = "vida"
    decesos = "decesos"
    salud = "salud"
    mascotas = "mascotas"
    autonomos = "autonomos"


class EstadoLeadEnum(str, Enum):
    nuevo = "nuevo"
    contactado = "contactado"
    en_proceso = "en_proceso"
    cotizado = "cotizado"
    cerrado_ganado = "cerrado_ganado"
    cerrado_perdido = "cerrado_perdido"


# ===========================================
# LEADS
# ===========================================

class LeadBase(BaseModel):
    """Schema base para leads"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo")
    email: EmailStr = Field(..., description="Email de contacto")
    telefono: str = Field(..., min_length=9, max_length=20, description="Teléfono")
    tipo_seguro: TipoSeguroEnum = Field(..., description="Tipo de seguro solicitado")
    mensaje: Optional[str] = Field(None, max_length=1000, description="Mensaje adicional")
    localidad: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=10)


class LeadCreate(LeadBase):
    """Schema para crear un nuevo lead desde el formulario"""
    # Datos de tracking opcionales
    origen: str = "web"
    landing_page: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None


class LeadUpdate(BaseModel):
    """Schema para actualizar un lead (CRM)"""
    estado: Optional[EstadoLeadEnum] = None
    asignado_a: Optional[str] = None
    notas_internas: Optional[str] = None


class LeadResponse(LeadBase):
    """Schema de respuesta con todos los datos"""
    id: int
    estado: str
    asignado_a: Optional[str]
    origen: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    """Lista paginada de leads"""
    total: int
    pagina: int
    por_pagina: int
    leads: List[LeadResponse]


# ===========================================
# CHATBOT IA
# ===========================================

class ChatMessage(BaseModel):
    """Mensaje del chat"""
    mensaje: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Respuesta del chatbot"""
    respuesta: str
    session_id: str
    sugerencias: Optional[List[str]] = None


# ===========================================
# BLOG
# ===========================================

class ArticuloBase(BaseModel):
    """Schema base para artículos"""
    titulo: str = Field(..., min_length=10, max_length=255)
    slug: str = Field(..., min_length=5, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=320)
    extracto: Optional[str] = None
    contenido: str
    categoria: Optional[str] = None
    tags: Optional[str] = None
    imagen_destacada: Optional[str] = None


class ArticuloCreate(ArticuloBase):
    """Crear artículo"""
    publicado: bool = False


class ArticuloResponse(ArticuloBase):
    """Respuesta de artículo"""
    id: int
    publicado: bool
    autor: str
    tiempo_lectura: int
    fecha_publicacion: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===========================================
# CONTACTO (formulario simple)
# ===========================================

class ContactoForm(BaseModel):
    """Formulario de contacto básico"""
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: str = Field(..., min_length=9, max_length=20)
    asunto: str = Field(..., min_length=5, max_length=200)
    mensaje: str = Field(..., min_length=10, max_length=2000)
    acepta_privacidad: bool = Field(..., description="Debe aceptar la política de privacidad")


class ContactoResponse(BaseModel):
    """Respuesta tras enviar contacto"""
    success: bool
    mensaje: str
    lead_id: Optional[int] = None


# ===========================================
# COMPARADOR
# ===========================================

class ComparadorForm(BaseModel):
    """Formulario del comparador de seguros"""
    # Paso 1: Tipo de seguro
    tipo_seguro: TipoSeguroEnum
    
    # Paso 2: Datos personales
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: str = Field(..., min_length=9, max_length=20)
    
    # Paso 3: Datos específicos (opcionales según tipo)
    fecha_nacimiento: Optional[str] = None
    codigo_postal: Optional[str] = None
    
    # Para seguro de hogar
    tipo_vivienda: Optional[str] = None  # piso, casa, chalet
    metros_cuadrados: Optional[int] = None
    es_propietario: Optional[bool] = None
    
    # Para seguro de auto
    marca_vehiculo: Optional[str] = None
    modelo_vehiculo: Optional[str] = None
    ano_vehiculo: Optional[int] = None
    
    # Tracking
    acepta_privacidad: bool = True


class ComparadorResponse(BaseModel):
    """Respuesta del comparador"""
    success: bool
    mensaje: str
    lead_id: int
    tiempo_respuesta: str = "24 horas"
