/**
 * Voice Input Handler for SupportGenie
 * Handles speech-to-text using Web Speech API
 * Supports multiple languages
 */

class VoiceInputHandler {
    constructor(inputElementId, buttonElementId, language = 'en') {
        this.inputElement = document.getElementById(inputElementId);
        this.buttonElement = document.getElementById(buttonElementId);
        this.language = language;
        this.isRecording = false;
        this.recognition = null;

        // Check browser support
        this.isSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;

        if (this.isSupported) {
            this.initializeRecognition();
        } else {
            console.warn('Speech recognition not supported in this browser');
        }
    }

    /**
     * Initialize speech recognition
     */
    initializeRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();

        // Language mapping
        const languageMap = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'te': 'te-IN'
        };

        this.recognition.lang = languageMap[this.language] || 'en-US';
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.maxAlternatives = 1;

        // Event handlers
        this.recognition.onstart = () => {
            this.isRecording = true;
            this.updateButtonState();
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.inputElement.value = transcript;

            // Trigger input event for auto-resize
            const inputEvent = new Event('input', { bubbles: true });
            this.inputElement.dispatchEvent(inputEvent);
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isRecording = false;
            this.updateButtonState();

            // Show error message
            this.showError(event.error);
        };

        this.recognition.onend = () => {
            this.isRecording = false;
            this.updateButtonState();
        };
    }

    /**
     * Start recording
     */
    startRecording() {
        if (!this.isSupported) {
            this.showError('not-supported');
            return;
        }

        if (this.isRecording) {
            this.stopRecording();
            return;
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
            this.showError('start-error');
        }
    }

    /**
     * Stop recording
     */
    stopRecording() {
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
        }
    }

    /**
     * Update button state
     */
    updateButtonState() {
        if (!this.buttonElement) return;

        if (this.isRecording) {
            this.buttonElement.classList.add('recording');
            this.buttonElement.innerHTML = `
                <svg class="w-6 h-6 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd"></path>
                </svg>
            `;
            this.buttonElement.title = 'Stop recording';
        } else {
            this.buttonElement.classList.remove('recording');
            this.buttonElement.innerHTML = `
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clip-rule="evenodd"></path>
                </svg>
            `;
            this.buttonElement.title = 'Voice input';
        }
    }

    /**
     * Show error message
     */
    showError(errorType) {
        const errorMessages = {
            'not-supported': 'Voice input is not supported in your browser. Please use Chrome, Edge, or Safari.',
            'no-speech': 'No speech detected. Please try again.',
            'audio-capture': 'Microphone access denied. Please allow microphone access.',
            'not-allowed': 'Microphone permission denied.',
            'start-error': 'Failed to start voice input. Please try again.',
            'network': 'Network error. Please check your connection.'
        };

        const message = errorMessages[errorType] || 'An error occurred with voice input.';

        // Create temporary error notification
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('animate-fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    /**
     * Change language
     */
    changeLanguage(language) {
        this.language = language;
        if (this.recognition) {
            const languageMap = {
                'en': 'en-US',
                'hi': 'hi-IN',
                'te': 'te-IN'
            };
            this.recognition.lang = languageMap[language] || 'en-US';
        }
    }

    /**
     * Check if voice input is supported
     */
    static isSupported() {
        return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceInputHandler;
}
