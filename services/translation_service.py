"""
Translation Service for SupportGenie
Handles multi-language support using Google Gemini API
Supports: English, Hindi, Telugu
"""

import google.generativeai as genai
import os
from typing import Dict, Optional
import json


class TranslationService:
    """Service for translating text between supported languages"""
    
    # Supported languages
    LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'te': 'Telugu'
    }
    
    def __init__(self, api_key: str = None):
        """Initialize Translation Service"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Cache for translations to reduce API calls
        self.cache = {}
    
    def translate(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (en, hi, te)
            source_language: Source language code (default: en)
            
        Returns:
            Translated text
        """
        # If same language, return original
        if source_language == target_language:
            return text
        
        # Check if language is supported
        if target_language not in self.LANGUAGES:
            return text
        
        # Check cache
        cache_key = f"{source_language}:{target_language}:{text[:50]}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            target_lang_name = self.LANGUAGES[target_language]
            source_lang_name = self.LANGUAGES.get(source_language, 'English')
            
            prompt = f"""Translate the following text from {source_lang_name} to {target_lang_name}.
Maintain the tone, style, and any emojis. Only provide the translation, no explanations.

Text to translate: {text}

Translation:"""
            
            response = self.model.generate_content(prompt)
            translated_text = response.text.strip()
            
            # Cache the result
            self.cache[cache_key] = translated_text
            
            return translated_text
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text on error
    
    def get_ui_translations(self, language: str) -> Dict[str, str]:
        """
        Get UI text translations for a specific language
        
        Args:
            language: Language code (en, hi, te)
            
        Returns:
            Dictionary of UI translations
        """
        translations = {
            'en': {
                'welcome': 'Welcome to SupportGenie!',
                'get_support': 'Get Support Now',
                'admin_dashboard': 'Admin Dashboard',
                'home': 'Home',
                'your_name': 'Your Name',
                'email_optional': 'Email (Optional)',
                'start_chat': 'Start Chat',
                'type_message': 'Type your message...',
                'send': 'Send',
                'return_product': 'Return Product',
                'create_ticket': 'Create Ticket',
                'request_call': 'Request Call',
                'upload_document': 'Upload Document',
                'analytics': 'Analytics',
                'knowledge_base': 'Knowledge Base',
                'customer_conversations': 'Customer Conversations',
                'all': 'All',
                'active': 'Active',
                'resolved': 'Resolved',
                'ai_assistant_online': 'AI Assistant - Online',
                'no_documents': 'No documents uploaded yet',
                'no_conversations': 'No conversations yet',
                'today_conversations': "Today's Conversations",
                'total_documents': 'Total Documents',
                'active_chats': 'Active Chats',
                'avg_response_time': 'Avg Response Time',
                'cancel': 'Cancel',
                'confirm': 'Confirm',
                'close': 'Close',
                'delete': 'Delete',
                'view': 'View',
                'export': 'Export',
            },
            'hi': {
                'welcome': 'SupportGenie में आपका स्वागत है!',
                'get_support': 'अभी सहायता प्राप्त करें',
                'admin_dashboard': 'प्रशासन डैशबोर्ड',
                'home': 'होम',
                'your_name': 'आपका नाम',
                'email_optional': 'ईमेल (वैकल्पिक)',
                'start_chat': 'चैट शुरू करें',
                'type_message': 'अपना संदेश टाइप करें...',
                'send': 'भेजें',
                'return_product': 'उत्पाद वापस करें',
                'create_ticket': 'टिकट बनाएं',
                'request_call': 'कॉल का अनुरोध करें',
                'upload_document': 'दस्तावेज़ अपलोड करें',
                'analytics': 'विश्लेषण',
                'knowledge_base': 'ज्ञान आधार',
                'customer_conversations': 'ग्राहक वार्तालाप',
                'all': 'सभी',
                'active': 'सक्रिय',
                'resolved': 'हल किया गया',
                'ai_assistant_online': 'AI सहायक - ऑनलाइन',
                'no_documents': 'अभी तक कोई दस्तावेज़ अपलोड नहीं किया गया',
                'no_conversations': 'अभी तक कोई वार्तालाप नहीं',
                'today_conversations': 'आज की बातचीत',
                'total_documents': 'कुल दस्तावेज़',
                'active_chats': 'सक्रिय चैट',
                'avg_response_time': 'औसत प्रतिक्रिया समय',
                'cancel': 'रद्द करें',
                'confirm': 'पुष्टि करें',
                'close': 'बंद करें',
                'delete': 'हटाएं',
                'view': 'देखें',
                'export': 'निर्यात करें',
            },
            'te': {
                'welcome': 'SupportGenie కి స్వాగతం!',
                'get_support': 'ఇప్పుడే మద్దతు పొందండి',
                'admin_dashboard': 'అడ్మిన్ డాష్‌బోర్డ్',
                'home': 'హోమ్',
                'your_name': 'మీ పేరు',
                'email_optional': 'ఇమెయిల్ (ఐచ్ఛికం)',
                'start_chat': 'చాట్ ప్రారంభించండి',
                'type_message': 'మీ సందేశాన్ని టైప్ చేయండి...',
                'send': 'పంపండి',
                'return_product': 'ఉత్పత్తిని తిరిగి ఇవ్వండి',
                'create_ticket': 'టికెట్ సృష్టించండి',
                'request_call': 'కాల్ అభ్యర్థించండి',
                'upload_document': 'పత్రాన్ని అప్‌లోడ్ చేయండి',
                'analytics': 'విశ్లేషణలు',
                'knowledge_base': 'జ్ఞాన స్థావరం',
                'customer_conversations': 'కస్టమర్ సంభాషణలు',
                'all': 'అన్నీ',
                'active': 'క్రియాశీల',
                'resolved': 'పరిష్కరించబడింది',
                'ai_assistant_online': 'AI అసిస్టెంట్ - ఆన్‌లైన్',
                'no_documents': 'ఇంకా పత్రాలు అప్‌లోడ్ చేయలేదు',
                'no_conversations': 'ఇంకా సంభాషణలు లేవు',
                'today_conversations': 'నేటి సంభాషణలు',
                'total_documents': 'మొత్తం పత్రాలు',
                'active_chats': 'క్రియాశీల చాట్‌లు',
                'avg_response_time': 'సగటు ప్రతిస్పందన సమయం',
                'cancel': 'రద్దు చేయండి',
                'confirm': 'నిర్ధారించండి',
                'close': 'మూసివేయండి',
                'delete': 'తొలగించండి',
                'view': 'చూడండి',
                'export': 'ఎగుమతి చేయండి',
            }
        }
        
        return translations.get(language, translations['en'])
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code (en, hi, te)
        """
        try:
            prompt = f"""Detect the language of the following text. 
Respond with ONLY one of these codes: en (English), hi (Hindi), or te (Telugu).
Do not provide any explanation, just the code.

Text: {text}

Language code:"""
            
            response = self.model.generate_content(prompt)
            detected = response.text.strip().lower()
            
            # Validate response
            if detected in self.LANGUAGES:
                return detected
            
            return 'en'  # Default to English
            
        except Exception as e:
            print(f"Language detection error: {e}")
            return 'en'  # Default to English on error
