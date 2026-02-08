#!/bin/bash
# Script de despliegue para Hostinger VPS

echo "🚀 Desplegando SegurosPy..."

# Actualizar código
git pull origin main

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Reiniciar servicio
sudo systemctl restart segurospy

echo "✅ Despliegue completado!"
