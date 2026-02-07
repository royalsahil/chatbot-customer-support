/**
 * Customer Support Chatbot - JavaScript
 * Handles chat functionality and API communication
 */

// Global state
let conversationHistory = [];
let currentConversationId = null;

/**
 * Initialize chat on page load
 */
document.addEventListener('DOMContentLoaded', function () {
    console.log('💬 Chatbot initialized');

    const userInput = document.getElementById('userInput');
    const chatForm = document.getElementById('chatForm');

    if (userInput) {
        userInput.focus();
        
        // Handle Enter key
        userInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    }

    if (chatForm) {
        chatForm.addEventListener('submit', sendMessage);
    }

    // Load conversation history from localStorage
    loadConversationHistory();
});

/**
 * Send message to chatbot
 */
async function sendMessage(event) {
    if (event) event.preventDefault();

    const input = document.getElementById('userInput');
    const message = input.value.trim();

    if (!message) return;

    // Clear input
    input.value = '';

    // Add user message to chat
    addUserMessage(message);

    // Show typing indicator
    showTypingIndicator();

    // Hide suggestions temporarily
    hideSuggestions();

    try {
        // Send message to API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Hide typing indicator
        hideTypingIndicator();

        if (data.success) {
            // Add bot response
            addBotMessage(data.response, data.intent, data.confidence);

            // Store conversation ID for feedback
            currentConversationId = data.conversation_id;

            // Update suggestions
            updateSuggestions(data.suggestions || []);

            // Save to conversation history
            saveToHistory(message, data.response);

            // Ensure focus input field
            input.focus();
        } else {
            throw new Error(data.error || 'Failed to get response');
        }

    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addBotMessage(
            "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.",
            'error',
            0
        );

        // Ensure focus input field even on error
        input.focus();
    }

    // Scroll to bottom
    scrollToBottom();
}

/**
 * Send a suggested question
 */
function sendSuggestion(message) {
    const input = document.getElementById('userInput');
    const form = document.getElementById('chatForm');

    if (input && form) {
        input.value = message;
        form.dispatchEvent(new Event('submit'));
        
        setTimeout(() => {
            input.focus();
        }, 100);
    }
}

/**
 * Add user message to chat
 */
function addUserMessage(message) {
    const messagesContainer = document.getElementById('chatMessages');
    const time = formatTime(new Date());

    const messageElement = document.createElement('div');
    messageElement.className = 'message user-message';
    messageElement.innerHTML = `
        <div class="message-avatar">
            <svg width="32" height="32" viewBox="0 0 40 40" fill="none">
                <circle cx="20" cy="20" r="20" fill="#667eea"/>
                <path d="M20 20C22.21 20 24 18.21 24 16C24 13.79 22.21 12 20 12C17.79 12 16 13.79 16 16C16 18.21 17.79 20 20 20ZM20 22C17.33 22 12 23.34 12 26V28H28V26C28 23.34 22.67 22 20 22Z" fill="white"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <p>${escapeHtml(message)}</p>
            </div>
            <div class="message-time">${time}</div>
        </div>
    `;

    messagesContainer.appendChild(messageElement);
    scrollToBottom();
}

/**
 * Add bot message to chat
 */
function addBotMessage(message, intent = '', confidence = 0) {
    const messagesContainer = document.getElementById('chatMessages');
    const time = formatTime(new Date());

    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message';

    // Format message (preserve line breaks and convert to HTML)
    const formattedMessage = formatBotMessage(message);

    messageElement.innerHTML = `
        <div class="message-avatar">
            <svg width="32" height="32" viewBox="0 0 40 40" fill="none">
                <circle cx="20" cy="20" r="20" fill="url(#gradient-${Date.now()})"/>
                <path d="M20 10C14.48 10 10 14.48 10 20C10 25.52 14.48 30 20 30C25.52 30 30 25.52 30 20C30 14.48 25.52 10 20 10Z" fill="white"/>
                <defs>
                    <linearGradient id="gradient-${Date.now()}" x1="0" y1="0" x2="40" y2="40">
                        <stop offset="0%" stop-color="#667eea"/>
                        <stop offset="100%" stop-color="#764ba2"/>
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                ${formattedMessage}
            </div>
            <div class="message-time">${time}</div>
        </div>
    `;

    messagesContainer.appendChild(messageElement);
    scrollToBottom();
}

/**
 * Format bot message (preserve line breaks, lists, etc.)
 */
function formatBotMessage(message) {
    // Escape HTML
    let formatted = escapeHtml(message);

    // Convert line breaks to <br>
    formatted = formatted.replace(/\n/g, '<br>');

    // Convert bullet points (- item or • item)
    formatted = formatted.replace(/^[-•]\s+(.+)$/gm, '<li>$1</li>');

    // Wrap lists in <ul>
    if (formatted.includes('<li>')) {
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }

    // Wrap in paragraph if no list
    if (!formatted.includes('<ul>')) {
        formatted = '<p>' + formatted + '</p>';
    }

    return formatted;
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'flex';
        scrollToBottom();
    }
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

/**
 * Update suggested questions
 */
function updateSuggestions(suggestions) {
    const container = document.getElementById('suggestions');

    if (!container) return;

    if (suggestions.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'flex';
    container.innerHTML = '';

    suggestions.forEach(suggestion => {
        const btn = document.createElement('button');
        btn.className = 'suggestion-btn';
        btn.textContent = suggestion;
        btn.onclick = () => sendSuggestion(suggestion);
        container.appendChild(btn);
    });
}

/**
 * Hide suggestions
 */
function hideSuggestions() {
    const container = document.getElementById('suggestions');
    if (container) container.style.display = 'none';
}

/**
 * Clear chat messages
 */
function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        const messagesContainer = document.getElementById('chatMessages');

        // Remove all messages except the welcome message
        const messages = messagesContainer.querySelectorAll('.message');
        messages.forEach((msg, index) => {
            if (index > 0) { // Keep first message (welcome)
                msg.remove();
            }
        });

        // Clear conversation history
        conversationHistory = [];
        localStorage.removeItem('chatHistory');

        // Reset suggestions to default
        updateSuggestions([
            'What is my order status?',
            'How can I cancel my order?',
            'What is your refund policy?',
            'How can I contact support?'
        ]);

        console.log('✓ Chat cleared');
    }
}

/**
 * Scroll to bottom of chat
 */
function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    if (messagesContainer) {
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }
}

/**
 * Format time
 */
function formatTime(date) {
    const now = new Date();
    const diff = Math.abs(now - date);

    // If less than 1 minute, show "Just now"
    if (diff < 60000) {
        return 'Just now';
    }

    // If less than 1 hour, show minutes
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} min ago`;
    }

    // Otherwise show time
    return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Save conversation to history
 */
function saveToHistory(userMessage, botResponse) {
    conversationHistory.push({
        user: userMessage,
        bot: botResponse,
        timestamp: new Date().toISOString()
    });

    // Keep only last 50 conversations
    if (conversationHistory.length > 50) {
        conversationHistory.shift();
    }

    // Save to localStorage
    try {
        localStorage.setItem('chatHistory', JSON.stringify(conversationHistory));
    } catch (e) {
        console.warn('Could not save to localStorage:', e);
    }
}

/**
 * Load conversation history from localStorage
 */
function loadConversationHistory() {
    try {
        const saved = localStorage.getItem('chatHistory');
        if (saved) {
            conversationHistory = JSON.parse(saved);
            console.log(`✓ Loaded ${conversationHistory.length} previous conversations`);
        }
    } catch (e) {
        console.warn('Could not load from localStorage:', e);
    }
}

/**
 * Send feedback for a conversation
 */
async function sendFeedback(conversationId, feedback) {
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                feedback: feedback
            })
        });

        const data = await response.json();

        if (data.success) {
            console.log('✓ Feedback sent');
        }
    } catch (error) {
        console.error('Error sending feedback:', error);
    }
}
