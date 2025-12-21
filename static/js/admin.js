/**
 * Admin Dashboard JavaScript
 * Handles all admin dashboard functionality
 */

// Global variables
let allConversations = [];
let currentFilter = 'all';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeAdmin();
    setupEventListeners();
    startAutoRefresh();
});

/**
 * Initialize admin dashboard
 */
async function initializeAdmin() {
    // Create language selector
    translationManager.createLanguageSelector('languageSelectorContainer');

    await loadAnalytics();
    await loadDocuments();
    await loadConversations();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Upload button
    document.getElementById('uploadBtn').addEventListener('click', () => {
        document.getElementById('uploadModal').classList.remove('hidden');
        document.getElementById('uploadModal').classList.add('flex');
    });

    // Cancel upload
    document.getElementById('cancelUpload').addEventListener('click', closeUploadModal);

    // Drop zone
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-purple-500', 'bg-purple-50');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-purple-500', 'bg-purple-50');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-purple-500', 'bg-purple-50');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Filter buttons
    document.getElementById('filterAll').addEventListener('click', () => filterConversations('all'));
    document.getElementById('filterActive').addEventListener('click', () => filterConversations('active'));
    document.getElementById('filterResolved').addEventListener('click', () => filterConversations('resolved'));

    // Close conversation modal
    document.getElementById('closeConversation').addEventListener('click', closeConversationModal);
}

/**
 * Load analytics data
 */
async function loadAnalytics() {
    try {
        const response = await fetch('/api/admin/analytics');
        const data = await response.json();

        if (data.success) {
            const analytics = data.analytics;
            document.getElementById('convToday').textContent = analytics.conversations_today;
            document.getElementById('totalDocs').textContent = analytics.total_documents;
            document.getElementById('activeChats').textContent = analytics.active_conversations;
            document.getElementById('avgResponse').textContent = analytics.avg_response_time + 's';
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

/**
 * Load documents
 */
async function loadDocuments() {
    try {
        const response = await fetch('/api/admin/documents');
        const data = await response.json();

        if (data.success) {
            displayDocuments(data.documents);
        }
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

/**
 * Display documents
 */
function displayDocuments(documents) {
    const container = document.getElementById('documentsList');
    const noDocsMsg = document.getElementById('noDocuments');

    if (documents.length === 0) {
        container.classList.add('hidden');
        noDocsMsg.classList.remove('hidden');
        return;
    }

    container.classList.remove('hidden');
    noDocsMsg.classList.add('hidden');

    container.innerHTML = documents.map(doc => `
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
            <div class="flex items-center space-x-3">
                <div class="text-2xl">📄</div>
                <div>
                    <p class="font-semibold text-gray-800">${doc.filename}</p>
                    <p class="text-xs text-gray-500">${formatDate(doc.uploaded_at)}</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <button class="text-purple-600 hover:text-purple-800 p-2" title="View">
                    👁️
                </button>
                <button class="delete-doc-btn text-red-600 hover:text-red-800 p-2" data-doc-id="${doc.id}" title="Delete">
                    🗑️
                </button>
            </div>
        </div>
    `).join('');

    // Add delete button event listeners
    document.querySelectorAll('.delete-doc-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const docId = btn.getAttribute('data-doc-id');
            deleteDocument(docId);
        });
    });
}

/**
 * Load conversations
 */
async function loadConversations() {
    try {
        const response = await fetch('/api/admin/conversations');
        const data = await response.json();

        if (data.success) {
            allConversations = data.conversations;
            filterConversations(currentFilter);
        }
    } catch (error) {
        console.error('Error loading conversations:', error);
    }
}

/**
 * Filter conversations
 */
function filterConversations(filter) {
    currentFilter = filter;

    // Update filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('bg-purple-600', 'text-white');
        btn.classList.add('bg-gray-200', 'text-gray-700');
    });

    const activeBtn = filter === 'all' ? 'filterAll' :
        filter === 'active' ? 'filterActive' : 'filterResolved';
    const btn = document.getElementById(activeBtn);
    btn.classList.add('bg-purple-600', 'text-white');
    btn.classList.remove('bg-gray-200', 'text-gray-700');

    // Filter conversations
    const filtered = filter === 'all' ? allConversations :
        allConversations.filter(c => c.status === filter);

    displayConversations(filtered);
}

/**
 * Display conversations
 */
function displayConversations(conversations) {
    const container = document.getElementById('conversationsList');
    const noConvMsg = document.getElementById('noConversations');

    if (conversations.length === 0) {
        container.classList.add('hidden');
        noConvMsg.classList.remove('hidden');
        return;
    }

    container.classList.remove('hidden');
    noConvMsg.classList.add('hidden');

    container.innerHTML = conversations.map(conv => `
        <div class="bg-gray-50 rounded-xl p-4 hover:bg-gray-100 transition cursor-pointer" onclick="viewConversation(${conv.id})">
            <div class="flex items-center justify-between">
                <div class="flex-1">
                    <div class="flex items-center space-x-3 mb-2">
                        <h3 class="font-bold text-gray-800">${conv.customer_name}</h3>
                        <span class="status-badge status-${conv.status}">${conv.status}</span>
                    </div>
                    <p class="text-sm text-gray-600">${conv.customer_email || 'No email provided'}</p>
                    <div class="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                        <span>💬 ${conv.message_count} messages</span>
                        <span>🕐 ${formatDate(conv.started_at)}</span>
                    </div>
                </div>
                <button class="px-4 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition">
                    View
                </button>
            </div>
        </div>
    `).join('');
}

/**
 * View conversation details
 */
async function viewConversation(conversationId) {
    try {
        const response = await fetch(`/api/admin/conversation/${conversationId}`);
        const data = await response.json();

        if (data.success) {
            displayConversationModal(data.conversation, data.messages);
        }
    } catch (error) {
        console.error('Error loading conversation:', error);
    }
}

/**
 * Display conversation modal
 */
function displayConversationModal(conversation, messages) {
    document.getElementById('modalCustomerName').textContent = conversation.customer_name;
    document.getElementById('modalCustomerEmail').textContent = conversation.customer_email || 'No email provided';

    const messagesContainer = document.getElementById('conversationMessages');
    messagesContainer.innerHTML = messages.map(msg => `
        <div class="flex ${msg.sender === 'customer' ? 'justify-end' : 'justify-start'}">
            <div class="max-w-[70%]">
                <div class="${msg.sender === 'ai' ? 'bg-gray-100' : 'bg-purple-600 text-white'} rounded-2xl px-4 py-3 ${msg.sender === 'ai' ? 'rounded-tl-none' : 'rounded-tr-none'}">
                    <p>${msg.message}</p>
                </div>
                <p class="text-xs text-gray-500 mt-1 ${msg.sender === 'customer' ? 'text-right' : ''}">${formatTimestamp(msg.timestamp)}</p>
            </div>
        </div>
    `).join('');

    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    document.getElementById('conversationModal').classList.remove('hidden');
    document.getElementById('conversationModal').classList.add('flex');
}

/**
 * Close conversation modal
 */
function closeConversationModal() {
    document.getElementById('conversationModal').classList.add('hidden');
    document.getElementById('conversationModal').classList.remove('flex');
}

/**
 * Handle file upload
 */
async function handleFileUpload(file) {
    if (file.size > 10 * 1024 * 1024) {
        alert('File too large. Maximum size is 10MB');
        return;
    }

    // Show progress
    document.getElementById('uploadProgress').classList.remove('hidden');
    document.getElementById('uploadSuccess').classList.add('hidden');

    const formData = new FormData();
    formData.append('document', file);

    try {
        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 10;
            document.getElementById('progressBar').style.width = progress + '%';
            if (progress >= 90) clearInterval(progressInterval);
        }, 100);

        const response = await fetch('/api/admin/upload-document', {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);
        document.getElementById('progressBar').style.width = '100%';

        const data = await response.json();

        if (data.success) {
            document.getElementById('uploadProgress').classList.add('hidden');
            document.getElementById('uploadSuccess').classList.remove('hidden');

            setTimeout(() => {
                closeUploadModal();
                loadDocuments();
                loadAnalytics();
            }, 2000);
        } else {
            alert('Upload failed: ' + data.error);
            document.getElementById('uploadProgress').classList.add('hidden');
        }
    } catch (error) {
        console.error('Upload error:', error);
        alert('Upload failed. Please try again.');
        document.getElementById('uploadProgress').classList.add('hidden');
    }
}

/**
 * Close upload modal
 */
function closeUploadModal() {
    document.getElementById('uploadModal').classList.add('hidden');
    document.getElementById('uploadModal').classList.remove('flex');
    document.getElementById('fileInput').value = '';
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('uploadProgress').classList.add('hidden');
    document.getElementById('uploadSuccess').classList.add('hidden');
}

/**
 * Start auto-refresh
 */
function startAutoRefresh() {
    setInterval(() => {
        loadAnalytics();
        loadConversations();
    }, 10000); // Refresh every 10 seconds
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;

    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;

    return date.toLocaleDateString();
}

/**
 * Format timestamp
 */
function formatTimestamp(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/**
 * Delete document
 */
async function deleteDocument(documentId) {
    // Confirm deletion
    if (!confirm('Are you sure you want to delete this document? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`/api/admin/delete-document/${documentId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            // Show success message
            showNotification('Document deleted successfully!', 'success');

            // Reload documents and analytics
            await loadDocuments();
            await loadAnalytics();
        } else {
            showNotification('Failed to delete document: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error deleting document:', error);
        showNotification('Error deleting document. Please try again.', 'error');
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const bgColors = {
        'success': 'bg-green-500',
        'error': 'bg-red-500',
        'info': 'bg-blue-500'
    };

    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${bgColors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('opacity-0');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
