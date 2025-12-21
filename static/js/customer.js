/**
 * Customer Chat JavaScript - Enhanced Version
 * Handles customer chat interface with multi-language and voice input support
 */

// Global variables
let conversationId = null;
let customerName = null;
let currentAction = null;
let currentLanguage = 'en';
let voiceHandler = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Get language from translation manager
    currentLanguage = translationManager.getCurrentLanguage();

    // Create language selector
    translationManager.createLanguageSelector('languageSelectorContainer');

    showWelcomeModal();
    setupEventListeners();

    // Initialize voice input
    if (VoiceInputHandler.isSupported()) {
        voiceHandler = new VoiceInputHandler('messageInput', 'voiceInputBtn', currentLanguage);
    } else {
        // Hide voice button if not supported
        document.getElementById('voiceInputBtn').style.display = 'none';
    }
});

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Start chat button
    document.getElementById('startChatBtn').addEventListener('click', startConversation);

    // Send message button
    document.getElementById('sendBtn').addEventListener('click', sendMessage);

    // Enter key in textarea
    document.getElementById('messageInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Voice input button
    const voiceBtn = document.getElementById('voiceInputBtn');
    if (voiceBtn) {
        voiceBtn.addEventListener('click', () => {
            if (voiceHandler) {
                voiceHandler.startRecording();
            }
        });
    }

    // Action buttons
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            showActionModal(action);
        });
    });

    // Action modal buttons
    document.getElementById('cancelAction').addEventListener('click', closeActionModal);
    document.getElementById('confirmAction').addEventListener('click', executeAction);
}

/**
 * Show welcome modal
 */
function showWelcomeModal() {
    document.getElementById('welcomeModal').style.display = 'flex';
}

/**
 * Start conversation
 */
async function startConversation() {
    const nameInput = document.getElementById('customerName');
    const emailInput = document.getElementById('customerEmail');

    const name = nameInput.value.trim();

    if (!name) {
        alert('Please enter your name');
        return;
    }

    customerName = name;
    const email = emailInput.value.trim() || null;

    try {
        const response = await fetch('/api/customer/start-conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                customer_name: name,
                customer_email: email,
                language: currentLanguage
            })
        });

        const data = await response.json();

        if (data.success) {
            conversationId = data.conversation_id;
            document.getElementById('welcomeModal').style.display = 'none';

            // Show AI welcome message in appropriate language
            const welcomeMessages = {
                'en': `Hi ${name}! 👋 I'm your SupportGenie assistant. How can I help you today?`,
                'hi': `नमस्ते ${name}! 👋 मैं आपका SupportGenie सहायक हूं। आज मैं आपकी कैसे मदद कर सकता हूं?`,
                'te': `హాయ్ ${name}! 👋 నేను మీ SupportGenie అసిస్టెంట్‌ని. ఈరోజు నేను మీకు ఎలా సహాయం చేయగలను?`
            };

            displayMessage('ai', welcomeMessages[currentLanguage] || welcomeMessages['en']);

            // Show quick actions
            document.getElementById('quickActions').classList.remove('hidden');
        } else {
            alert('Failed to start conversation: ' + data.error);
        }
    } catch (error) {
        console.error('Error starting conversation:', error);
        alert('Failed to start conversation. Please try again.');
    }
}

/**
 * Send message
 */
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message || !conversationId) return;

    // Display user message immediately
    displayMessage('customer', message);
    input.value = '';

    // Auto-resize textarea
    input.style.height = 'auto';

    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch('/api/customer/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                message: message
            })
        });

        const data = await response.json();

        hideTypingIndicator();

        if (data.success) {
            // Display AI response
            displayMessage('ai', data.ai_response);

            // Handle action if taken
            if (data.action_taken) {
                displayActionResult(data.action_taken);
            }
        } else {
            const errorMessages = {
                'en': 'Sorry, I encountered an error. Please try again. 😔',
                'hi': 'क्षमा करें, मुझे एक त्रुटि का सामना करना पड़ा। कृपया पुनः प्रयास करें। 😔',
                'te': 'క్షమించండి, నాకు ఒక లోపం ఎదురైంది. దయచేసి మళ్లీ ప్రయత్నించండి. 😔'
            };
            displayMessage('ai', errorMessages[currentLanguage] || errorMessages['en']);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        const errorMessages = {
            'en': 'Sorry, I encountered an error. Please try again. 😔',
            'hi': 'क्षमा करें, मुझे एक त्रुटि का सामना करना पड़ा। कृपया पुनः प्रयास करें। 😔',
            'te': 'క్షమించండి, నాకు ఒక లోపం ఎదురైంది. దయచేసి మళ్లీ ప్రయత్నించండి. 😔'
        };
        displayMessage('ai', errorMessages[currentLanguage] || errorMessages['en']);
    }
}

/**
 * Display message
 */
function displayMessage(sender, message) {
    const container = document.getElementById('messagesContainer');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-enter';

    if (sender === 'ai') {
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-purple-700 flex items-center justify-center text-white flex-shrink-0">
                    🤖
                </div>
                <div class="flex-1">
                    <div class="bg-white rounded-2xl rounded-tl-none px-4 py-3 shadow-md max-w-[80%]">
                        <p class="text-gray-800">${message}</p>
                    </div>
                    <p class="text-xs text-gray-500 mt-1 ml-2">${getCurrentTime()}</p>
                </div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3 justify-end">
                <div class="flex-1 flex justify-end">
                    <div class="bg-gradient-to-r from-purple-600 to-purple-700 rounded-2xl rounded-tr-none px-4 py-3 shadow-md max-w-[80%]">
                        <p class="text-white">${message}</p>
                    </div>
                </div>
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-400 to-gray-600 flex items-center justify-center text-white flex-shrink-0">
                    👤
                </div>
            </div>
            <p class="text-xs text-gray-500 mt-1 mr-14 text-right">${getCurrentTime()}</p>
        `;
    }

    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    document.getElementById('typingIndicator').classList.remove('hidden');
    const container = document.getElementById('messagesContainer');
    container.scrollTop = container.scrollHeight;
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    document.getElementById('typingIndicator').classList.add('hidden');
}

/**
 * Show action modal
 */
function showActionModal(action) {
    currentAction = action;
    const modal = document.getElementById('actionModal');
    const title = document.getElementById('actionTitle');
    const description = document.getElementById('actionDescription');
    const form = document.getElementById('actionForm');

    // Set content based on action type
    switch (action) {
        case 'return_product':
            title.textContent = '🔄 Return Product';
            description.textContent = 'Provide details for your return request';
            form.innerHTML = `
                <input type="text" id="returnOrderId" placeholder="Order ID" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 mb-3">
                <input type="text" id="productName" placeholder="Product Name" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 mb-3">
                <textarea id="returnReason" placeholder="Reason for return" rows="3"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500"></textarea>
            `;
            break;

        case 'create_ticket':
            title.textContent = '🎫 Create Support Ticket';
            description.textContent = 'Would you like me to create a support ticket? Our team will respond within 24 hours.';
            form.innerHTML = `
                <textarea id="ticketSummary" placeholder="Describe your issue..." rows="4"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 mb-3"></textarea>
                <select id="ticketPriority" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500">
                    <option value="low">Low Priority</option>
                    <option value="medium" selected>Medium Priority</option>
                    <option value="high">High Priority</option>
                </select>
            `;
            break;

        case 'request_call':
            title.textContent = '📞 Request Callback';
            description.textContent = 'Our team will call you at your preferred time';
            form.innerHTML = `
                <input type="tel" id="phoneNumber" placeholder="Phone Number" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 mb-3">
                <input type="text" id="preferredTime" placeholder="Preferred Time (e.g., 2 PM - 4 PM)" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 mb-3">
                <textarea id="callReason" placeholder="Reason for call..." rows="3"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500"></textarea>
            `;
            break;
    }

    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

/**
 * Close action modal
 */
function closeActionModal() {
    document.getElementById('actionModal').classList.add('hidden');
    document.getElementById('actionModal').classList.remove('flex');
}

/**
 * Execute action
 */
async function executeAction() {
    if (!currentAction || !conversationId) return;

    let actionData = {};

    // Collect data based on action type
    switch (currentAction) {
        case 'return_product':
            actionData.order_id = document.getElementById('returnOrderId').value;
            actionData.product = document.getElementById('productName').value;
            actionData.reason = document.getElementById('returnReason').value;
            break;

        case 'create_ticket':
            actionData.summary = document.getElementById('ticketSummary').value;
            actionData.priority = document.getElementById('ticketPriority').value;
            break;

        case 'request_call':
            const phoneNumber = document.getElementById('phoneNumber').value;
            const preferredTime = document.getElementById('preferredTime').value;
            const reason = document.getElementById('callReason').value;

            if (!phoneNumber) {
                alert('Please enter your phone number');
                return;
            }

            // Handle call request separately
            closeActionModal();
            showTypingIndicator();

            try {
                const response = await fetch('/api/customer/request-call', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        conversation_id: conversationId,
                        customer_name: customerName,
                        customer_email: document.getElementById('customerEmail')?.value || '',
                        phone_number: phoneNumber,
                        preferred_time: preferredTime || 'ASAP',
                        reason: reason || 'Customer requested callback'
                    })
                });

                const data = await response.json();
                hideTypingIndicator();

                if (data.success) {
                    const successMessages = {
                        'en': '✅ Call request submitted! Our team will contact you soon at ' + phoneNumber,
                        'hi': '✅ कॉल अनुरोध सबमिट किया गया! हमारी टीम जल्द ही आपसे संपर्क करेगी ' + phoneNumber,
                        'te': '✅ కాల్ అభ్యర్థన సమర్పించబడింది! మా బృందం త్వరలో మిమ్మల్ని సంప్రదిస్తుంది ' + phoneNumber
                    };
                    displayMessage('ai', successMessages[currentLanguage] || successMessages['en']);
                } else {
                    displayMessage('ai', 'Sorry, failed to submit call request. Please try again.');
                }
            } catch (error) {
                console.error('Error requesting call:', error);
                hideTypingIndicator();
                displayMessage('ai', 'Sorry, encountered an error. Please try again.');
            }
            return;
    }

    closeActionModal();
    showTypingIndicator();

    try {
        const response = await fetch('/api/customer/execute-action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                action_type: currentAction,
                action_data: actionData
            })
        });

        const data = await response.json();

        hideTypingIndicator();

        if (data.success) {
            displayActionResult({ type: currentAction, result: data });
        } else {
            displayMessage('ai', 'Sorry, I couldn\'t complete that action. Please try again.');
        }
    } catch (error) {
        console.error('Error executing action:', error);
        hideTypingIndicator();
        displayMessage('ai', 'Sorry, I encountered an error. Please try again.');
    }
}

/**
 * Display action result
 */
function displayActionResult(actionTaken) {
    const { type, result } = actionTaken;
    let message = result.message || 'Action completed successfully!';

    // Add additional info based on action type
    if (type === 'create_ticket' && result.ticket_data) {
        message += `\n\nTicket ID: ${result.ticket_data.ticket_id}`;
    } else if (type === 'return_product' && result.return_data) {
        message += `\n\nRMA Number: ${result.return_data.rma_number}`;
    }

    displayMessage('ai', message);
}

/**
 * Get current time
 */
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/**
 * Auto-resize textarea
 */
const textarea = document.getElementById('messageInput');
if (textarea) {
    textarea.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });
}
