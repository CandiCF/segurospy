"""
Modelos de Base de Datos - SQLAlchemy
Equivalente a las estructuras de datos que manejas en Google Sheets/n8n
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class TipoSeguro(enum.Enum):
    """Tipos de seguros disponibles"""
    HOGAR = "hogar"
    AUTO = "auto"
    VIDA = "vida"
    DECESOS = "decesos"
    SALUD = "salud"
    MASCOTAS = "mascotas"
    AUTONOMOS = "autonomos"


class EstadoLead(enum.Enum):
    """Estados del lead en el funnel"""
    NUEVO = "nuevo"
    CONTACTADO = "contactado"
    EN_PROCESO = "en_proceso"
    COTIZADO = "cotizado"
    CERRADO_GANADO = "cerrado_ganado"
    CERRADO_PERDIDO = "cerrado_perdido"


class Lead(Base):
    """
    Modelo de Lead - Equivalente a lo que guardas en Google Sheets
    """
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos personales
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    telefono = Column(String(20), nullable=False)
    
    # Datos del seguro
    tipo_seguro = Column(String(50), nullable=False)
    mensaje = Column(Text, nullable=True)
    
    # Datos de localización (SEO local)
    localidad = Column(String(100), nullable=True)
    codigo_postal = Column(String(10), nullable=True)
    
    # Estado y seguimiento
    estado = Column(String(50), default="nuevo")
    asignado_a = Column(String(100), nullable=True)
    notas_internas = Column(Text, nullable=True)
    
    # Origen del lead
    origen = Column(String(100), default="web")  # web, comparador, landing, etc.
    landing_page = Column(String(255), nullable=True)
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    
    # Metadatos
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    contacted_at = Column(DateTime, nullable=True)
    
    # Relaciones
    conversaciones = relationship("Conversacion", back_populates="lead")
    
    def __repr__(self):
        return f"<Lead {self.nombre} - {self.tipo_seguro}>"


class Conversacion(Base):
    """
    Historial de conversaciones del chatbot IA
    """
    __tablename__ = "conversaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    
    session_id = Column(String(100), nullable=False, index=True)
    rol = Column(String(20), nullable=False)  # user, assistant
    mensaje = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    lead = relationship("Lead", back_populates="conversaciones")


class ArticuloBlog(Base):
    """
    Artículos del blog - En vez de archivos HTML estáticos
    """
    __tablename__ = "articulos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # SEO
    slug = Column(String(255), unique=True, nullable=False, index=True)
    titulo = Column(String(255), nullable=False)
    meta_description = Column(String(320), nullable=True)
    keywords = Column(String(500), nullable=True)
    
    # Contenido
    extracto = Column(Text, nullable=True)
    contenido = Column(Text, nullable=False)
    imagen_destacada = Column(String(255), nullable=True)
    
    # Categorización
    categoria = Column(String(100), nullable=True)
    tags = Column(String(500), nullable=True)
    
    # Publicación
    publicado = Column(Boolean, default=False)
    fecha_publicacion = Column(DateTime, nullable=True)
    
    # Metadatos
    autor = Column(String(100), default="SegurosPy")
    tiempo_lectura = Column(Integer, default=5)  # minutos
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SolicitudResena(Base):
    """
    Control de solicitudes de reseñas enviadas
    """
    __tablename__ = "solicitudes_resena"
    
    id = Column(Integer, primary_key=True, index=True)
    
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    email_enviado = Column(Boolean, default=False)
    fecha_envio = Column(DateTime, nullable=True)
    
    # Seguimiento
    abierto = Column(Boolean, default=False)
    clicked = Column(Boolean, default=False)
    resena_dejada = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class ConfiguracionSEO(Base):
    """
    Configuración SEO por página (equivalente a los meta tags en HTML)
    """
    __tablename__ = "configuracion_seo"
    
    id = Column(Integer, primary_key=True, index=True)
    
    pagina = Column(String(100), unique=True, nullable=False)  # home, seguro-hogar, etc.
    titulo = Column(String(70), nullable=False)
    meta_description = Column(String(160), nullable=False)
    og_title = Column(String(70), nullable=True)
    og_description = Column(String(200), nullable=True)
    og_image = Column(String(255), nullable=True)
    canonical_url = Column(String(255), nullable=True)
    
    # Schema JSON-LD
    schema_json = Column(Text, nullable=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
