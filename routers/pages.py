"""
Router de Páginas - Renderiza las vistas HTML con Jinja2
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Páginas"])

# Configurar templates
templates = Jinja2Templates(directory="templates")


# =============================================
# PÁGINAS PRINCIPALES
# =============================================

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal"""
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "titulo": "SegurosPy - Tu Agente de Seguros en Madrid",
            "meta_description": "Correduría de seguros en Madrid. Comparamos más de 20 aseguradoras para ofrecerte el mejor precio en seguros de hogar, auto, vida y más."
        }
    )


@router.get("/seguro-hogar", response_class=HTMLResponse)
async def seguro_hogar(request: Request):
    """Página de seguro de hogar"""
    return templates.TemplateResponse(
        "pages/seguro-hogar.html",
        {
            "request": request,
            "titulo": "Seguro de Hogar en Madrid | SegurosPy",
            "meta_description": "Protege tu hogar con las mejores coberturas. Comparamos todas las aseguradoras para encontrarte el mejor precio."
        }
    )


@router.get("/seguro-coche", response_class=HTMLResponse)
async def seguro_coche(request: Request):
    """Página de seguro de coche"""
    return templates.TemplateResponse(
        "pages/seguro-coche.html",
        {
            "request": request,
            "titulo": "Seguro de Coche en Madrid | SegurosPy",
            "meta_description": "Ahorra hasta un 40% en tu seguro de coche. Terceros, todo riesgo y franquicia. Comparamos más de 20 aseguradoras."
        }
    )


@router.get("/seguro-vida", response_class=HTMLResponse)
async def seguro_vida(request: Request):
    """Página de seguro de vida"""
    return templates.TemplateResponse(
        "pages/seguro-vida.html",
        {
            "request": request,
            "titulo": "Seguro de Vida en Madrid | SegurosPy",
            "meta_description": "Protege el futuro de tu familia con un seguro de vida. Desde 10€/mes. Asesoramiento gratuito."
        }
    )


@router.get("/seguro-decesos", response_class=HTMLResponse)
async def seguro_decesos(request: Request):
    """Página de seguro de decesos"""
    return templates.TemplateResponse(
        "pages/seguro-decesos.html",
        {
            "request": request,
            "titulo": "Seguro de Decesos en Madrid | SegurosPy",
            "meta_description": "Tranquilidad para ti y tu familia. Seguro de decesos con todas las gestiones incluidas. Consulta sin compromiso."
        }
    )


@router.get("/seguro-salud", response_class=HTMLResponse)
async def seguro_salud(request: Request):
    """Página de seguro de salud"""
    return templates.TemplateResponse(
        "pages/seguro-salud.html",
        {
            "request": request,
            "titulo": "Seguro de Salud en Madrid | SegurosPy",
            "meta_description": "Accede a los mejores especialistas sin esperas. Seguros de salud adaptados a tus necesidades."
        }
    )


@router.get("/comparador", response_class=HTMLResponse)
async def comparador(request: Request):
    """Comparador de seguros"""
    return templates.TemplateResponse(
        "pages/comparador.html",
        {
            "request": request,
            "titulo": "Comparador de Seguros en Madrid | SegurosPy",
            "meta_description": "Compara seguros de auto, hogar, vida y más. Más de 20 aseguradoras. Cotización en 2 minutos."
        }
    )


@router.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    """Blog de seguros"""
    return templates.TemplateResponse(
        "pages/blog.html",
        {
            "request": request,
            "titulo": "Blog de Seguros | SegurosPy",
            "meta_description": "Artículos y guías sobre seguros. Aprende a elegir el mejor seguro para ti."
        }
    )


@router.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    """Página de contacto"""
    return templates.TemplateResponse(
        "pages/contacto.html",
        {
            "request": request,
            "titulo": "Contacto | SegurosPy",
            "meta_description": "Contacta con SegurosPy. Teléfono: 661 854 126. Email: info@segurospy.com"
        }
    )


@router.get("/politica-privacidad", response_class=HTMLResponse)
async def privacidad(request: Request):
    """Política de privacidad"""
    return templates.TemplateResponse(
        "pages/privacidad.html",
        {
            "request": request,
            "titulo": "Política de Privacidad | SegurosPy",
            "meta_description": "Política de privacidad y protección de datos de SegurosPy."
        }
    )
