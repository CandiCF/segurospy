/**
 * SegurosPy - JavaScript Principal
 */

// =============================================
// CHAT WIDGET
// =============================================

let sessionId = null;

function toggleChat() {
    const widget = document.querySelector('.chat-window');
    const icon = document.querySelector('.chat-icon');
    const close = document.querySelector('.chat-close');

    if (widget.style.display === 'none' || !widget.style.display) {
        widget.style.display = 'flex';
        icon.style.display = 'none';
        close.style.display = 'block';
    } else {
        widget.style.display = 'none';
        icon.style.display = 'block';
        close.style.display = 'none';
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

    // Añadir mensaje del usuario
    addMessage(mensaje, 'user');
    input.value = '';

    // Mostrar indicador de escritura
    addTypingIndicator();

    try {
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: mensaje,
                session_id: sessionId
            })
        });

        const data = await response.json();

        // Guardar session_id
        sessionId = data.session_id;

        // Quitar indicador y añadir respuesta
        removeTypingIndicator();
        addMessage(data.respuesta, 'bot');

        // Añadir sugerencias si existen
        if (data.sugerencias && data.sugerencias.length > 0) {
            addSuggestions(data.sugerencias);
        }

    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo.', 'bot');
    }
}

function addMessage(text, type) {
    const container = document.getElementById('chat-messages');
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    container.appendChild(message);
    container.scrollTop = container.scrollHeight;
}

function addTypingIndicator() {
    const container = document.getElementById('chat-messages');
    const indicator = document.createElement('div');
    indicator.className = 'message bot typing';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = '<span>•</span><span>•</span><span>•</span>';
    container.appendChild(indicator);
    container.scrollTop = container.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function addSuggestions(suggestions) {
    const container = document.getElementById('chat-messages');
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'chat-suggestions';

    suggestions.forEach(text => {
        const btn = document.createElement('button');
        btn.className = 'suggestion-btn';
        btn.textContent = text;
        btn.onclick = () => {
            document.getElementById('chat-input').value = text;
            sendMessage();
        };
        suggestionsDiv.appendChild(btn);
    });

    container.appendChild(suggestionsDiv);
    container.scrollTop = container.scrollHeight;
}


// =============================================
// MOBILE MENU
// =============================================

document.querySelector('.mobile-menu-btn')?.addEventListener('click', function () {
    const nav = document.querySelector('.nav-links');
    nav.classList.toggle('active');
    this.classList.toggle('active');
});


// =============================================
// SMOOTH SCROLL
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
// FORM VALIDATION HELPERS
// =============================================

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const cleaned = phone.replace(/\s/g, '');
    return cleaned.length >= 9 && /^\d+$/.test(cleaned);
}


// =============================================
// ANIMATIONS ON SCROLL
// =============================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

document.querySelectorAll('.service-card, .feature, .stat').forEach(el => {
    observer.observe(el);
});


// =============================================
// CONSOLE EASTER EGG
// =============================================

console.log(`
🐍 SegurosPy - Desarrollado con Python + FastAPI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Eres desarrollador? ¡Contáctanos!
📧 info@segurospy.com
`);
