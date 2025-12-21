/**
 * Translation Manager for SupportGenie
 * Handles multi-language support (English, Hindi, Telugu)
 */

class TranslationManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('supportgenie_language') || 'en';
        this.translations = {};
        this.loadTranslations();
    }

    /**
     * Load translations from server
     */
    async loadTranslations() {
        try {
            const response = await fetch(`/api/translations/${this.currentLanguage}`);
            const data = await response.json();

            if (data.success) {
                this.translations = data.translations;
                this.applyTranslations();
            }
        } catch (error) {
            console.error('Error loading translations:', error);
        }
    }

    /**
     * Change language
     */
    async changeLanguage(language) {
        if (language === this.currentLanguage) return;

        this.currentLanguage = language;
        localStorage.setItem('supportgenie_language', language);

        await this.loadTranslations();

        // Reload page to apply language change
        window.location.reload();
    }

    /**
     * Get current language
     */
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    /**
     * Get translation for a key
     */
    t(key) {
        return this.translations[key] || key;
    }

    /**
     * Apply translations to page
     */
    applyTranslations() {
        // Update all elements with data-translate attribute
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.t(key);

            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
    }

    /**
     * Create language selector
     */
    createLanguageSelector(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const languages = {
            'en': { name: 'English', flag: '🇬🇧' },
            'hi': { name: 'हिंदी', flag: '🇮🇳' },
            'te': { name: 'తెలుగు', flag: '🇮🇳' }
        };

        const selectorHTML = `
            <div class="language-selector relative">
                <button id="languageButton" class="flex items-center space-x-2 px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg transition">
                    <span class="text-xl">${languages[this.currentLanguage].flag}</span>
                    <span class="font-semibold">${languages[this.currentLanguage].name}</span>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </button>
                <div id="languageDropdown" class="hidden absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl z-50">
                    ${Object.entries(languages).map(([code, lang]) => `
                        <button class="language-option w-full flex items-center space-x-3 px-4 py-3 hover:bg-gray-100 transition ${code === this.currentLanguage ? 'bg-purple-50' : ''}"
                                data-language="${code}">
                            <span class="text-2xl">${lang.flag}</span>
                            <span class="font-semibold text-gray-800">${lang.name}</span>
                            ${code === this.currentLanguage ? '<span class="ml-auto text-purple-600">✓</span>' : ''}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;

        container.innerHTML = selectorHTML;

        // Setup event listeners
        const button = document.getElementById('languageButton');
        const dropdown = document.getElementById('languageDropdown');

        button.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('hidden');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            dropdown.classList.add('hidden');
        });

        // Language option click handlers
        document.querySelectorAll('.language-option').forEach(option => {
            option.addEventListener('click', async (e) => {
                e.stopPropagation();
                const language = option.getAttribute('data-language');
                await this.changeLanguage(language);
            });
        });
    }
}

// Create global translation manager instance
const translationManager = new TranslationManager();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TranslationManager;
}
