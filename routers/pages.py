"""
Router de Páginas - Renderiza las vistas HTML con Jinja2
Enfocado en Sierra de Madrid Noroeste
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Páginas"])

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Zona de servicio
ZONA = "Sierra de Madrid"
LOCALIDADES = "Villalba, Galapagar, Alpedrete, Torrelodones, Guadarrama, Los Molinos y Cercedilla"


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
            "titulo": f"SegurosPy - Tu Agente de Seguros en la {ZONA} 💜",
            "meta_description": f"Agente de seguros en {LOCALIDADES}. Comparamos más de 20 aseguradoras para ofrecerte el mejor precio. ¡Ahorra hasta un 40%!"
        }
    )


@router.get("/seguro-hogar", response_class=HTMLResponse)
async def seguro_hogar(request: Request):
    """Página de seguro de hogar"""
    return templates.TemplateResponse(
        "pages/seguro-hogar.html",
        {
            "request": request,
            "titulo": f"Seguro de Hogar en {ZONA} | SegurosPy",
            "meta_description": f"Protege tu hogar en {LOCALIDADES}. Comparamos todas las aseguradoras para encontrarte el mejor precio."
        }
    )


@router.get("/seguro-coche", response_class=HTMLResponse)
async def seguro_coche(request: Request):
    """Página de seguro de coche"""
    return templates.TemplateResponse(
        "pages/seguro-coche.html",
        {
            "request": request,
            "titulo": f"Seguro de Coche en {ZONA} | SegurosPy",
            "meta_description": f"Ahorra hasta un 40% en tu seguro de coche en {LOCALIDADES}. Terceros, todo riesgo y franquicia."
        }
    )


@router.get("/seguro-vida", response_class=HTMLResponse)
async def seguro_vida(request: Request):
    """Página de seguro de vida"""
    return templates.TemplateResponse(
        "pages/seguro-vida.html",
        {
            "request": request,
            "titulo": f"Seguro de Vida en {ZONA} | SegurosPy",
            "meta_description": f"Protege el futuro de tu familia con un seguro de vida. Asesoramiento gratuito en {LOCALIDADES}."
        }
    )


@router.get("/seguro-decesos", response_class=HTMLResponse)
async def seguro_decesos(request: Request):
    """Página de seguro de decesos"""
    return templates.TemplateResponse(
        "pages/seguro-decesos.html",
        {
            "request": request,
            "titulo": f"Seguro de Decesos en {ZONA} | SegurosPy",
            "meta_description": f"Tranquilidad para ti y tu familia en {LOCALIDADES}. Seguro de decesos con todas las gestiones incluidas."
        }
    )


@router.get("/seguro-salud", response_class=HTMLResponse)
async def seguro_salud(request: Request):
    """Página de seguro de salud"""
    return templates.TemplateResponse(
        "pages/seguro-salud.html",
        {
            "request": request,
            "titulo": f"Seguro de Salud en {ZONA} | SegurosPy",
            "meta_description": f"Accede a los mejores especialistas sin esperas. Seguros de salud en {LOCALIDADES}."
        }
    )


@router.get("/seguro-mujer", response_class=HTMLResponse)
async def seguro_mujer(request: Request):
    """Página de seguro exclusivo para mujeres - Producto estrella"""
    return templates.TemplateResponse(
        "pages/seguro-mujer.html",
        {
            "request": request,
            "titulo": f"Seguro Exclusivo para Ti que Eres Mujer | {ZONA} | SegurosPy",
            "meta_description": f"Seguro exclusivo para mujeres con asistencia oncológica, vida diaria, gestión de sucesiones y bonus por no siniestralidad. Villalba, Galapagar y Sierra de Madrid."
        }
    )


@router.get("/comparador", response_class=HTMLResponse)
async def comparador(request: Request):
    """Comparador de seguros"""
    return templates.TemplateResponse(
        "pages/comparador.html",
        {
            "request": request,
            "titulo": f"Comparador de Seguros en {ZONA} | SegurosPy",
            "meta_description": f"Compara seguros en {LOCALIDADES}. Más de 20 aseguradoras. Cotización en 2 minutos."
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
            "meta_description": f"Contacta con SegurosPy. Teléfono: 647 801 213. Email: norte.oficina.villalba@gmail.com. {LOCALIDADES}"
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


# =============================================
# ARTÍCULOS DEL BLOG - SEO
# =============================================

@router.get("/blog/seguro-hogar-villalba-guia-completa", response_class=HTMLResponse)
async def blog_seguro_hogar_villalba(request: Request):
    """Artículo SEO: Seguro de hogar en Collado Villalba"""
    return templates.TemplateResponse(
        "pages/blog/seguro-hogar-villalba-guia-completa.html",
        {
            "request": request,
            "titulo": "Seguro de Hogar en Collado Villalba: Guía Completa 2024 | SegurosPy",
            "meta_description": "Todo sobre seguro de hogar en Collado Villalba, Galapagar, Alpedrete y Sierra de Madrid. Coberturas, precios y cómo ahorrar hasta 40%."
        }
    )


@router.get("/blog/seguro-coche-galapagar-mejores-ofertas", response_class=HTMLResponse)
async def blog_seguro_coche_galapagar(request: Request):
    """Artículo SEO: Seguro de coche en Galapagar"""
    return templates.TemplateResponse(
        "pages/blog/seguro-coche-galapagar-mejores-ofertas.html",
        {
            "request": request,
            "titulo": "Seguro de Coche en Galapagar: Mejores Ofertas 2024 | SegurosPy",
            "meta_description": "Compara seguros de coche en Galapagar, Villalba y Sierra de Madrid. Terceros desde 180€/año. Todo riesgo con franquicia al mejor precio."
        }
    )


@router.get("/blog/seguro-decesos-sierra-madrid-todo-incluido", response_class=HTMLResponse)
async def blog_seguro_decesos(request: Request):
    """Artículo SEO: Seguro de decesos en la Sierra de Madrid"""
    return templates.TemplateResponse(
        "pages/blog/seguro-decesos-sierra-madrid-todo-incluido.html",
        {
            "request": request,
            "titulo": "Seguro de Decesos en Sierra de Madrid: ¿Qué Incluye? | SegurosPy",
            "meta_description": "Descubre qué cubre el seguro de decesos. Servicio 24h, traslados, gestiones incluidas. Desde 5€/mes en Villalba, Galapagar y toda la Sierra."
        }
    )


@router.get("/blog/seguro-mujer-coberturas-exclusivas", response_class=HTMLResponse)
async def blog_seguro_mujer(request: Request):
    """Artículo SEO: Seguro exclusivo para mujeres"""
    return templates.TemplateResponse(
        "pages/blog/seguro-mujer-coberturas-exclusivas.html",
        {
            "request": request,
            "titulo": "Seguro Exclusivo para Mujeres: 6 Coberturas que No Conocías | SegurosPy",
            "meta_description": "Seguro exclusivo para mujeres con asistencia oncológica, vida diaria, gestión de sucesiones y más. Pensado para ti, trabajes o no."
        }
    )


@router.get("/blog/como-ahorrar-seguro-hogar-alpedrete", response_class=HTMLResponse)
async def blog_ahorrar_seguro(request: Request):
    """Artículo SEO: Cómo ahorrar en seguro de hogar"""
    return templates.TemplateResponse(
        "pages/blog/como-ahorrar-seguro-hogar-alpedrete.html",
        {
            "request": request,
            "titulo": "Cómo Ahorrar en tu Seguro de Hogar en Alpedrete y Torrelodones | SegurosPy",
            "meta_description": "7 trucos para reducir la prima de tu seguro de hogar sin perder coberturas. Ahorra hasta 200€ al año en la Sierra de Madrid."
        }
    )


@router.get("/blog/seguro-mascotas-sierra-guadarrama", response_class=HTMLResponse)
async def blog_seguro_mascotas(request: Request):
    """Artículo SEO: Seguro de mascotas en la Sierra"""
    return templates.TemplateResponse(
        "pages/blog/seguro-mascotas-sierra-guadarrama.html",
        {
            "request": request,
            "titulo": "Seguro de Mascotas en Sierra de Guadarrama: Guía 2024 | SegurosPy",
            "meta_description": "Protege a tu perro o gato. Seguro de mascotas con cobertura veterinaria, responsabilidad civil y asistencia en viaje. Sierra de Madrid."
        }
    )
