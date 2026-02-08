/**
 * SegurosPy - JavaScript Principal
 * Diseño vibrante y alegre para Sierra de Madrid
 */

// Variables globales
let chatSessionId = null;

// =============================================
// CHAT WIDGET
// =============================================

function toggleChat() {
    const chatWindow = document.querySelector('.chat-window');
    const chatIcon = document.querySelector('.chat-icon');
    const chatClose = document.querySelector('.chat-close');

    if (chatWindow.style.display === 'none' || !chatWindow.style.display) {
        chatWindow.style.display = 'flex';
        chatIcon.style.display = 'none';
        chatClose.style.display = 'block';
        document.getElementById('chat-input').focus();
    } else {
        chatWindow.style.display = 'none';
        chatIcon.style.display = 'block';
        chatClose.style.display = 'none';
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const mensaje = input.value.trim();

    if (!mensaje) return;

    // Mostrar mensaje del usuario
    addMessage(mensaje, 'user');
    input.value = '';

    // Mostrar indicador de escritura
    showTyping();

    try {
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: mensaje,
                session_id: chatSessionId
            })
        });

        const data = await response.json();

        // Ocultar indicador de escritura
        hideTyping();

        if (data.respuesta) {
            addMessage(data.respuesta, 'bot');
            if (data.session_id) {
                chatSessionId = data.session_id;
            }

            // Mostrar sugerencias si las hay
            if (data.sugerencias && data.sugerencias.length > 0) {
                addSuggestions(data.sugerencias);
            }
        }
    } catch (error) {
        hideTyping();
        addMessage('Lo siento, ha ocurrido un error. ¿Puedes intentarlo de nuevo? 💜', 'bot');
        console.error('Error:', error);
    }
}

function addMessage(text, type) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTyping() {
    const messagesContainer = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = '<span>●</span><span>●</span><span>●</span>';
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTyping() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function addSuggestions(sugerencias) {
    const messagesContainer = document.getElementById('chat-messages');
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'chat-suggestions';

    sugerencias.forEach(sug => {
        const btn = document.createElement('button');
        btn.className = 'suggestion-btn';
        btn.textContent = sug;
        btn.onclick = () => {
            document.getElementById('chat-input').value = sug;
            sendMessage();
            suggestionsDiv.remove();
        };
        suggestionsDiv.appendChild(btn);
    });

    messagesContainer.appendChild(suggestionsDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// =============================================
// NAVEGACIÓN MÓVIL
// =============================================

document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.dropdown');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function () {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Manejar clics en dropdowns para móvil
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function (e) {
            if (window.innerWidth <= 1024) {
                // Prevenir navegación si es un dropdown en móvil
                const menu = this.querySelector('.dropdown-menu');
                if (menu) {
                    e.preventDefault();
                    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
                }
            }
        });
    });

    // Cerrar menú al hacer clic en un enlace (que no sea un dropdown)
    if (navLinks) {
        navLinks.querySelectorAll('a:not(#dropdown-toggle)').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                if (mobileMenuBtn) mobileMenuBtn.classList.remove('active');
            });
        });
    }

    // Animaciones de entrada
    observeElements();
});

// =============================================
// SCROLL SUAVE
// =============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// =============================================
// ANIMACIONES DE ENTRADA
// =============================================

function observeElements() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observar elementos
    document.querySelectorAll('.service-card, .feature, .stat, .form-group').forEach(el => {
        observer.observe(el);
    });
}

// =============================================
// UTILIDADES
// =============================================

// Formatear teléfono mientras se escribe
document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener('input', function (e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 9) value = value.slice(0, 9);
        e.target.value = value;
    });
});

// Prevenir doble envío de formularios
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function () {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            setTimeout(() => {
                submitBtn.disabled = true;
            }, 100);
        }
    });
});

console.log('🛡️ SegurosPy cargado - Sierra de Madrid 💜');
