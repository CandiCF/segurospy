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

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function () {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Cerrar menú al hacer clic en un enlace
    if (navLinks) {
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
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
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        observer.observe(el);
    });
}

// =============================================
// CSS ADICIONAL VIA JS
// =============================================

const additionalStyles = document.createElement('style');
additionalStyles.textContent = `
    /* Navegación móvil */
    @media (max-width: 768px) {
        .nav-links {
            position: fixed;
            top: 70px;
            left: 0;
            right: 0;
            background: white;
            flex-direction: column;
            padding: 1rem;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.2);
            transform: translateY(-110%);
            transition: transform 0.3s ease;
            z-index: 99;
        }
        
        .nav-links.active {
            transform: translateY(0);
        }
        
        .mobile-menu-btn.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .mobile-menu-btn.active span:nth-child(2) {
            opacity: 0;
        }
        
        .mobile-menu-btn.active span:nth-child(3) {
            transform: rotate(-45deg) translate(5px, -5px);
        }
        
        .dropdown-menu {
            position: static;
            transform: none;
            box-shadow: none;
            opacity: 1;
            visibility: visible;
            padding: 0.5rem 0 0 1rem;
            border: none;
        }
    }
    
    /* Indicador de escritura del chat */
    .typing span {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin: 0 2px;
        background: #FF6B6B;
        border-radius: 50%;
        animation: typingBounce 1.4s infinite ease-in-out both;
    }
    
    .typing span:nth-child(1) { animation-delay: -0.32s; }
    .typing span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typingBounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    /* Sugerencias del chat */
    .chat-suggestions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .suggestion-btn {
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #FFE4E1, #FFF0F5);
        border: 2px solid #FF6B6B;
        border-radius: 999px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #FF6B6B;
        font-weight: 500;
    }
    
    .suggestion-btn:hover {
        background: linear-gradient(135deg, #FF6B6B, #FF69B4);
        color: white;
        transform: scale(1.05);
    }
    
    /* Animación de entrada */
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
`;
document.head.appendChild(additionalStyles);

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
