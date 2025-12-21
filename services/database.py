"""
Database service for SupportGenie
Handles all SQLite database operations
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os


class Database:
    """Database management class for SupportGenie"""
    
    def __init__(self, db_path: str = "database/supportgenie.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def _init_database(self):
        """Create all necessary tables"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_content TEXT,
                    structured_content TEXT,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    deleted_at TIMESTAMP DEFAULT NULL
                )
            """)
            
            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT,
                    language TEXT DEFAULT 'en',
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    satisfaction_rating INTEGER
                )
            """)
            
            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    sender TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source_document_id INTEGER,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            
            # Actions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    action_type TEXT NOT NULL,
                    action_data TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def save_document(self, filename: str, original_content: str, structured_content: str) -> int:
        """Save a document to the database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO documents (filename, original_content, structured_content)
                VALUES (?, ?, ?)
            """, (filename, original_content, structured_content))
            
            document_id = cursor.lastrowid
            conn.commit()
            return document_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_all_documents(self) -> List[Dict]:
        """Get all documents from the database (excluding deleted)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, filename, uploaded_at 
                FROM documents 
                WHERE deleted_at IS NULL
                ORDER BY uploaded_at DESC
            """)
            
            documents = []
            for row in cursor.fetchall():
                documents.append({
                    'id': row['id'],
                    'filename': row['filename'],
                    'uploaded_at': row['uploaded_at']
                })
            
            return documents
        finally:
            conn.close()
    
    def get_document_by_id(self, document_id: int) -> Optional[Dict]:
        """Get a specific document by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, filename, original_content, structured_content, uploaded_at
                FROM documents
                WHERE id = ?
            """, (document_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'filename': row['filename'],
                    'original_content': row['original_content'],
                    'structured_content': row['structured_content'],
                    'uploaded_at': row['uploaded_at']
                }
            return None
        finally:
            conn.close()
    
    def search_documents(self, keywords: List[str]) -> List[Dict]:
        """Search documents by keywords"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Build search query
            query = """
                SELECT id, filename, structured_content
                FROM documents
                WHERE """
            
            conditions = []
            params = []
            
            for keyword in keywords:
                conditions.append("(structured_content LIKE ? OR filename LIKE ?)")
                params.extend([f"%{keyword}%", f"%{keyword}%"])
            
            query += " OR ".join(conditions)
            query += " LIMIT 3"
            
            cursor.execute(query, params)
            
            documents = []
            for row in cursor.fetchall():
                documents.append({
                    'id': row['id'],
                    'filename': row['filename'],
                    'content': row['structured_content']
                })
            
            return documents
        finally:
            conn.close()
    
    def create_conversation(self, customer_name: str, customer_email: str = None, language: str = 'en') -> int:
        """Create a new conversation"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO conversations (customer_name, customer_email, language)
                VALUES (?, ?, ?)
            """, (customer_name, customer_email, language))
            
            conversation_id = cursor.lastrowid
            conn.commit()
            return conversation_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def save_message(self, conversation_id: int, sender: str, message: str, 
                     source_document_id: int = None) -> int:
        """Save a message to a conversation"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO messages (conversation_id, sender, message, source_document_id)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, sender, message, source_document_id))
            
            message_id = cursor.lastrowid
            conn.commit()
            return message_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_conversation_messages(self, conversation_id: int) -> List[Dict]:
        """Get all messages for a conversation"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, sender, message, timestamp, source_document_id
                FROM messages
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
            """, (conversation_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'id': row['id'],
                    'sender': row['sender'],
                    'message': row['message'],
                    'timestamp': row['timestamp'],
                    'source_document_id': row['source_document_id']
                })
            
            return messages
        finally:
            conn.close()
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations with message counts"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    c.id,
                    c.customer_name,
                    c.customer_email,
                    c.started_at,
                    c.status,
                    c.satisfaction_rating,
                    COUNT(m.id) as message_count
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                GROUP BY c.id
                ORDER BY c.started_at DESC
            """)
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    'id': row['id'],
                    'customer_name': row['customer_name'],
                    'customer_email': row['customer_email'],
                    'started_at': row['started_at'],
                    'status': row['status'],
                    'satisfaction_rating': row['satisfaction_rating'],
                    'message_count': row['message_count']
                })
            
            return conversations
        finally:
            conn.close()
    
    def get_conversation_by_id(self, conversation_id: int) -> Optional[Dict]:
        """Get a specific conversation by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, customer_name, customer_email, started_at, status, satisfaction_rating
                FROM conversations
                WHERE id = ?
            """, (conversation_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'customer_name': row['customer_name'],
                    'customer_email': row['customer_email'],
                    'started_at': row['started_at'],
                    'status': row['status'],
                    'satisfaction_rating': row['satisfaction_rating']
                }
            return None
        finally:
            conn.close()
    
    def update_conversation_status(self, conversation_id: int, status: str):
        """Update conversation status"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE conversations
                SET status = ?
                WHERE id = ?
            """, (status, conversation_id))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def create_action(self, conversation_id: int, action_type: str, action_data: Dict) -> int:
        """Create an action"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO actions (conversation_id, action_type, action_data)
                VALUES (?, ?, ?)
            """, (conversation_id, action_type, json.dumps(action_data)))
            
            action_id = cursor.lastrowid
            conn.commit()
            return action_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def update_action_status(self, action_id: int, status: str):
        """Update action status"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE actions
                SET status = ?
                WHERE id = ?
            """, (status, action_id))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_analytics(self) -> Dict:
        """Get analytics data for admin dashboard"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Total conversations today
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM conversations
                WHERE DATE(started_at) = DATE('now')
            """)
            conversations_today = cursor.fetchone()['count']
            
            # Total documents
            cursor.execute("SELECT COUNT(*) as count FROM documents WHERE deleted_at IS NULL")
            total_documents = cursor.fetchone()['count']
            
            # Active conversations
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM conversations
                WHERE status = 'active'
            """)
            active_conversations = cursor.fetchone()['count']
            
            # Average response time (mock for demo - 2.5 seconds)
            avg_response_time = 2.5
            
            return {
                'conversations_today': conversations_today,
                'total_documents': total_documents,
                'active_conversations': active_conversations,
                'avg_response_time': avg_response_time
            }
        finally:
            conn.close()
    
    def delete_document(self, document_id: int) -> bool:
        """
        Soft delete a document
        
        Args:
            document_id: ID of document to delete
            
        Returns:
            True if deleted successfully
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE documents
                SET deleted_at = CURRENT_TIMESTAMP
                WHERE id = ? AND deleted_at IS NULL
            """, (document_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_conversation_language(self, conversation_id: int) -> str:
        """
        Get the language preference for a conversation
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            Language code (en, hi, te)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT language
                FROM conversations
                WHERE id = ?
            """, (conversation_id,))
            
            row = cursor.fetchone()
            return row['language'] if row else 'en'
        finally:
            conn.close()
