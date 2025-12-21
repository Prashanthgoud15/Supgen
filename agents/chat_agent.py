"""
Chat Agent for SupportGenie
Handles customer conversations with context-aware responses
"""

from typing import List, Dict
from services.gemini_service import GeminiService
from services.database import Database


class ChatAgent:
    """Agent responsible for handling customer conversations"""
    
    def __init__(self, gemini_service: GeminiService, database: Database):
        """Initialize Chat Agent with required services"""
        self.gemini = gemini_service
        self.db = database
    
    def handle_message(self, conversation_id: int, user_message: str) -> Dict[str, any]:
        """
        Handle incoming customer message
        
        Args:
            conversation_id: ID of the conversation
            user_message: Message from the customer
            
        Returns:
            Dict with AI response and relevant metadata
        """
        try:
            # Get conversation language
            language = self.db.get_conversation_language(conversation_id)
            
            # Save user message to database
            self.db.save_message(
                conversation_id=conversation_id,
                sender='customer',
                message=user_message
            )
            
            # Get conversation history
            conversation_history = self.db.get_conversation_messages(conversation_id)
            
            # Search for relevant documents
            relevant_documents = self._search_relevant_documents(user_message)
            
            # Generate AI response using Gemini with language support
            ai_response = self.gemini.generate_response(
                user_message=user_message,
                document_context=relevant_documents,
                conversation_history=conversation_history,
                language=language
            )
            
            # Determine source document (if any)
            source_doc_id = relevant_documents[0]['id'] if relevant_documents else None
            
            # Save AI response to database
            self.db.save_message(
                conversation_id=conversation_id,
                sender='ai',
                message=ai_response,
                source_document_id=source_doc_id
            )
            
            return {
                'success': True,
                'response': ai_response,
                'source_documents': [doc['filename'] for doc in relevant_documents] if relevant_documents else [],
                'language': language
            }
            
        except Exception as e:
            print(f"Error handling message: {e}")
            # Error messages in different languages
            error_messages = {
                'en': "I apologize, but I'm having trouble processing your message. Please try again.",
                'hi': "मुझे खेद है, लेकिन मुझे आपके संदेश को संसाधित करने में परेशानी हो रही है। कृपया पुनः प्रयास करें।",
                'te': "క్షమించండి, కానీ నేను మీ సందేశాన్ని ప్రాసెస్ చేయడంలో ఇబ్బంది పడుతున్నాను. దయచేసి మళ్లీ ప్రయత్నించండి."
            }
            language = self.db.get_conversation_language(conversation_id) if conversation_id else 'en'
            return {
                'success': False,
                'response': error_messages.get(language, error_messages['en']),
                'error': str(e)
            }
    
    def _search_relevant_documents(self, user_message: str) -> List[Dict]:
        """
        Search for documents relevant to the user's message
        Uses simple keyword-based search
        
        Args:
            user_message: The customer's message
            
        Returns:
            List of relevant documents with content
        """
        # Extract keywords (simple approach - split and filter)
        keywords = self._extract_keywords(user_message)
        
        if not keywords:
            return []
        
        # Search documents in database
        documents = self.db.search_documents(keywords)
        
        # Limit context size
        limited_docs = []
        total_chars = 0
        max_chars = 8000  # Limit to prevent token overflow
        
        for doc in documents:
            doc_chars = len(doc.get('content', ''))
            if total_chars + doc_chars < max_chars:
                limited_docs.append(doc)
                total_chars += doc_chars
            else:
                # Truncate last document
                remaining = max_chars - total_chars
                if remaining > 500:  # Only add if meaningful
                    doc['content'] = doc['content'][:remaining]
                    limited_docs.append(doc)
                break
        
        return limited_docs
    
    def _extract_keywords(self, message: str) -> List[str]:
        """
        Extract keywords from user message
        Simple approach: filter out common words, take significant terms
        
        Args:
            message: User's message
            
        Returns:
            List of keywords
        """
        # Common stop words to ignore
        stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
            'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
            'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
            'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
            'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
            'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
            'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
            'once', 'can', 'will', 'just', 'should', 'now', 'how', 'where', 'when'
        }
        
        # Split message into words and filter
        words = message.lower().split()
        keywords = []
        
        for word in words:
            # Remove punctuation
            clean_word = ''.join(char for char in word if char.isalnum())
            
            # Keep if not a stop word and length > 2
            if clean_word and clean_word not in stop_words and len(clean_word) > 2:
                keywords.append(clean_word)
        
        # Return unique keywords (max 5 most relevant)
        return list(set(keywords))[:5]
    
    def get_conversation_history(self, conversation_id: int) -> List[Dict]:
        """Get full conversation history"""
        return self.db.get_conversation_messages(conversation_id)
