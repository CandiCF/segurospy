# 🚀 Guía de Despliegue en Hostinger VPS

## Requisitos
- Hostinger VPS (Ubuntu 22.04 recomendado)
- Dominio segurospy.com configurado

---

## 1️⃣ Configurar VPS

### Conectar por SSH
```bash
ssh root@tu_ip_vps
```

### Actualizar sistema
```bash
apt update && apt upgrade -y
```

### Instalar dependencias
```bash
apt install python3.11 python3.11-venv python3-pip nginx git -y
```

---

## 2️⃣ Clonar Proyecto

```bash
# Crear directorio
mkdir -p /var/www
cd /var/www

# Clonar repositorio
git clone https://github.com/CandiCF/segurospy.git
cd segurospy

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 3️⃣ Configurar Variables de Entorno

```bash
# Copiar archivo de configuración
cp .env.production .env

# Editar con tus valores
nano .env
```

Configura:
- `SMTP_PASSWORD`: Contraseña de aplicación de Gmail
- `OPENAI_API_KEY`: Tu API key de OpenAI (opcional para chatbot)
- `SECRET_KEY`: Genera una clave aleatoria

---

## 4️⃣ Configurar Servicio Systemd

```bash
# Copiar archivo de servicio
cp segurospy.service /etc/systemd/system/

# Recargar systemd
systemctl daemon-reload

# Iniciar servicio
systemctl start segurospy
systemctl enable segurospy

# Verificar estado
systemctl status segurospy
```

---

## 5️⃣ Configurar Nginx

```bash
nano /etc/nginx/sites-available/segurospy
```

Contenido:
```nginx
server {
    listen 80;
    server_name segurospy.com www.segurospy.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /static {
        alias /var/www/segurospy/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Activar sitio
ln -s /etc/nginx/sites-available/segurospy /etc/nginx/sites-enabled/

# Verificar configuración
nginx -t

# Reiniciar Nginx
systemctl restart nginx
```

---

## 6️⃣ Configurar SSL (HTTPS)

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx -y

# Obtener certificado SSL
certbot --nginx -d segurospy.com -d www.segurospy.com

# Renovación automática
certbot renew --dry-run
```

---

## 7️⃣ Configurar Dominio en Hostinger

En el panel de Hostinger:
1. Ve a **Dominios** → **segurospy.com**
2. Configura los **DNS**:
   - Tipo A: `@` → IP del VPS
   - Tipo A: `www` → IP del VPS

---

## 8️⃣ Verificar Despliegue

```bash
# Ver logs
journalctl -u segurospy -f

# Probar localmente
curl http://127.0.0.1:8000
```

Visita: https://segurospy.com

---

## 🔄 Actualizar Código

```bash
cd /var/www/segurospy
./deploy.sh
```

---

## 📋 Comandos Útiles

```bash
# Ver estado del servicio
systemctl status segurospy

# Reiniciar aplicación
systemctl restart segurospy

# Ver logs en tiempo real
journalctl -u segurospy -f

# Ver logs de Nginx
tail -f /var/log/nginx/error.log
```

---

## ⚠️ Solución de Problemas

### La aplicación no arranca
```bash
# Verificar logs
journalctl -u segurospy --no-pager -n 50

# Probar manualmente
cd /var/www/segurospy
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Error 502 Bad Gateway
```bash
# Verificar que el servicio está corriendo
systemctl status segurospy

# Reiniciar
systemctl restart segurospy
systemctl restart nginx
```

### Error de permisos
```bash
chown -R www-data:www-data /var/www/segurospy
chmod -R 755 /var/www/segurospy
```

---

## 📞 Contacto
- Email: norte.oficina.villalba@gmail.com
- Teléfono: 647 801 213
