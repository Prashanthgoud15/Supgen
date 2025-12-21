"""
Gemini AI Service for SupportGenie
Handles all interactions with Google Gemini API
"""

import google.generativeai as genai
import os
from typing import List, Dict, Optional
import re


class GeminiService:
    """Service class for Google Gemini AI integration"""
    
    def __init__(self, api_key: str = None):
        """Initialize Gemini API"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def process_document(self, text_content: str) -> str:
        """
        Process raw PDF text into structured content
        Returns organized sections for easy retrieval
        """
        prompt = f"""
You are a document processing assistant. Analyze the following document and extract information into these structured sections:

**PRODUCT_INFO**: Product name, model, specifications, features
**COMMON_ISSUES**: Frequently asked questions and common problems
**WARRANTY**: Warranty information, terms, conditions
**TROUBLESHOOTING**: Step-by-step troubleshooting guides
**CONTACT**: Contact information, support channels

Format each section clearly with headers. If a section has no relevant information, write "Not available".

Document Content:
{text_content[:15000]}

Provide the structured output:
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error processing document: {e}")
            return f"Error processing document: {str(e)}"
    
    def generate_response(self, user_message: str, document_context: List[Dict], 
                         conversation_history: List[Dict], language: str = 'en') -> str:
        """
        Generate AI response to customer query
        Uses document context and conversation history
        Responds in the specified language
        """
        # Build context from documents
        context_text = ""
        if document_context:
            context_text = "\n\n=== KNOWLEDGE BASE ===\n"
            for doc in document_context:
                context_text += f"\nDocument: {doc.get('filename', 'Unknown')}\n"
                content = doc.get('content', '')
                # Limit context to prevent token overflow
                context_text += content[:3000] + "\n---\n"
        
        # Build conversation history
        history_text = ""
        if conversation_history:
            history_text = "\n\n=== CONVERSATION HISTORY ===\n"
            for msg in conversation_history[-5:]:  # Last 5 messages
                sender = msg.get('sender', 'unknown')
                text = msg.get('message', '')
                history_text += f"{sender.upper()}: {text}\n"
        
        # Language-specific instructions
        language_names = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu'
        }
        target_language = language_names.get(language, 'English')
        
        # System prompt with improved grounding
        system_prompt = f"""You are SupportGenie, a friendly and helpful AI customer support assistant.

CRITICAL RULES:
- ONLY answer questions based on the knowledge base provided
- If information is NOT in the knowledge base, say "I don't have that information in my knowledge base"
- NEVER make up or guess information
- Be honest when you don't know something
- Respond ONLY in {target_language}

Your role:
- Provide accurate answers STRICTLY based on the knowledge base
- Be empathetic and understanding
- Ask clarifying questions when needed
- Offer to create support tickets when you cannot help
- Keep responses concise and natural (2-3 sentences usually)
- If you cannot answer from the knowledge base, offer to escalate

Response style:
- Conversational and warm (use emojis occasionally 😊)
- Professional but friendly
- Break complex answers into steps
- Always offer next steps or ask if they need more help

When to suggest actions:
- Customer wants to return/exchange → offer "return_product" action
- Issue cannot be resolved from knowledge base → offer "create_ticket" action

REMEMBER: Respond in {target_language} language ONLY."""
        
        # Build full prompt
        full_prompt = f"""{system_prompt}

{context_text}

{history_text}

CUSTOMER: {user_message}

Provide a helpful response in {target_language}:"""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            # Error messages in different languages
            error_messages = {
                'en': "I apologize, but I'm having trouble processing your request right now. Could you please try again? 😊",
                'hi': "मुझे खेद है, लेकिन मुझे अभी आपके अनुरोध को संसाधित करने में परेशानी हो रही है। क्या आप कृपया पुनः प्रयास कर सकते हैं? 😊",
                'te': "క్షమించండి, కానీ నేను ప్రస్తుతం మీ అభ్యర్థనను ప్రాసెస్ చేయడంలో ఇబ్బంది పడుతున్నాను. దయచేసి మళ్లీ ప్రయత్నించగలరా? 😊"
            }
            return error_messages.get(language, error_messages['en'])
    
    def detect_intent(self, user_message: str) -> Dict[str, any]:
        """
        Detect user intent and extract entities
        Returns: {intent: str, entities: dict, confidence: float}
        """
        prompt = f"""Analyze this customer message and determine their intent.

Message: "{user_message}"

Classify the intent as ONE of:
- return_product: Customer wants to return/exchange a product
- check_order: Customer wants order status/tracking
- create_ticket: Customer has a complex issue needing human support
- general_query: General question or support request

Also extract any relevant entities like:
- product_name
- order_id
- problem_description

Respond in this exact format:
INTENT: <intent>
ENTITIES: <key=value pairs or "none">
CONFIDENCE: <high/medium/low>"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Parse response
            intent_match = re.search(r'INTENT:\s*(\w+)', text)
            intent = intent_match.group(1) if intent_match else 'general_query'
            
            confidence_match = re.search(r'CONFIDENCE:\s*(\w+)', text)
            confidence = confidence_match.group(1) if confidence_match else 'medium'
            
            # Extract entities (simple parsing)
            entities = {}
            entities_match = re.search(r'ENTITIES:\s*(.+?)(?:\n|$)', text)
            if entities_match and entities_match.group(1).lower() != 'none':
                entities_text = entities_match.group(1)
                # Simple key=value parsing
                for pair in entities_text.split(','):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        entities[key.strip()] = value.strip()
            
            return {
                'intent': intent,
                'entities': entities,
                'confidence': confidence
            }
        except Exception as e:
            print(f"Error detecting intent: {e}")
            return {
                'intent': 'general_query',
                'entities': {},
                'confidence': 'low'
            }
    
    def draft_email(self, context: str, purpose: str) -> str:
        """
        Draft a professional email for customer support
        """
        prompt = f"""Draft a professional customer support email.

Purpose: {purpose}
Context: {context}

Write a complete email with:
- Professional greeting
- Clear explanation
- Next steps
- Professional closing

Keep it concise and friendly."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error drafting email: {e}")
            return "Error drafting email"
