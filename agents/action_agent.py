"""
Action Agent for SupportGenie
Handles autonomous actions like creating tickets, drafting emails, etc.
"""

from typing import Dict
from services.gemini_service import GeminiService
from services.database import Database
from services.email_service import EmailService
import random


class ActionAgent:
    """Agent responsible for executing autonomous actions"""
    
    def __init__(self, gemini_service: GeminiService, database: Database):
        """Initialize Action Agent with required services"""
        self.gemini = gemini_service
        self.db = database
        self.email_service = EmailService()
    
    def execute_action(self, conversation_id: int, action_type: str, 
                       action_data: Dict = None) -> Dict[str, any]:
        """
        Execute a specific action based on type
        
        Args:
            conversation_id: ID of the conversation
            action_type: Type of action to execute
            action_data: Additional data for the action
            
        Returns:
            Dict with action result and status
        """
        action_data = action_data or {}
        
        # Create action record in database
        action_id = self.db.create_action(
            conversation_id=conversation_id,
            action_type=action_type,
            action_data=action_data
        )
        
        try:
            result = None
            
            if action_type == 'create_ticket':
                result = self._create_ticket(conversation_id, action_data)
            elif action_type == 'draft_email':
                result = self._draft_email(conversation_id, action_data)
            elif action_type == 'check_order':
                result = self._check_order(action_data)
            elif action_type == 'return_product':
                result = self._return_product(action_data)
            else:
                result = {
                    'success': False,
                    'message': f'Unknown action type: {action_type}'
                }
            
            # Update action status
            status = 'completed' if result.get('success') else 'failed'
            self.db.update_action_status(action_id, status)
            
            result['action_id'] = action_id
            return result
            
        except Exception as e:
            self.db.update_action_status(action_id, 'failed')
            return {
                'success': False,
                'message': f'Error executing action: {str(e)}',
                'action_id': action_id
            }
    
    def _create_ticket(self, conversation_id: int, data: Dict) -> Dict:
        """
        Create a support ticket for escalation
        
        Args:
            conversation_id: ID of the conversation
            data: Ticket data
            
        Returns:
            Ticket creation result
        """
        # Get conversation details
        conversation = self.db.get_conversation_by_id(conversation_id)
        messages = self.db.get_conversation_messages(conversation_id)
        
        # Generate ticket ID (mock for demo)
        ticket_id = f"TKT-{random.randint(10000, 99999)}"
        
        # Build ticket summary
        issue_summary = data.get('summary', 'Customer support required')
        
        ticket_data = {
            'ticket_id': ticket_id,
            'customer_name': conversation['customer_name'],
            'customer_email': conversation['customer_email'],
            'issue_summary': issue_summary,
            'priority': data.get('priority', 'medium'),
            'message_count': len(messages),
            'status': 'open'
        }
        
        # Send email notification to admin
        try:
            self.email_service.send_support_ticket_notification(ticket_data, messages)
            print(f"✅ Email notification sent for ticket {ticket_id}")
        except Exception as e:
            print(f"⚠️ Failed to send email notification: {e}")
        
        return {
            'success': True,
            'message': f'Support ticket {ticket_id} created successfully! Our team will respond within 24 hours.',
            'ticket_data': ticket_data
        }
    
    def _draft_email(self, conversation_id: int, data: Dict) -> Dict:
        """
        Draft a professional email using Gemini
        
        Args:
            conversation_id: ID of the conversation
            data: Email context data
            
        Returns:
            Drafted email
        """
        # Get conversation context
        messages = self.db.get_conversation_messages(conversation_id)
        conversation = self.db.get_conversation_by_id(conversation_id)
        
        # Build context for email
        context = f"Customer: {conversation['customer_name']}\n"
        if messages:
            last_messages = messages[-3:]
            context += "Recent conversation:\n"
            for msg in last_messages:
                context += f"- {msg['sender']}: {msg['message']}\n"
        
        purpose = data.get('purpose', 'Follow up on customer inquiry')
        
        # Generate email using Gemini
        email_content = self.gemini.draft_email(context, purpose)
        
        return {
            'success': True,
            'message': 'Email drafted successfully!',
            'email_content': email_content,
            'recipient': conversation['customer_email']
        }
    
    def _check_order(self, data: Dict) -> Dict:
        """
        Check order status (mock implementation for demo)
        
        Args:
            data: Order data (order_id, etc.)
            
        Returns:
            Order status information
        """
        order_id = data.get('order_id', f'ORD-{random.randint(1000, 9999)}')
        
        # Mock order statuses
        statuses = [
            'Processing - Expected ship date: Tomorrow',
            'Shipped - Tracking #: TRK123456789, Arriving in 2-3 days',
            'Out for Delivery - Expected today by 8 PM',
            'Delivered - Signed by: Resident'
        ]
        
        status = random.choice(statuses)
        
        order_data = {
            'order_id': order_id,
            'status': status,
            'items': data.get('items', 'Product items'),
            'total': data.get('total', '$99.99')
        }
        
        return {
            'success': True,
            'message': f'Order {order_id} status: {status}',
            'order_data': order_data
        }
    
    def _return_product(self, data: Dict) -> Dict:
        """
        Initiate product return process
        
        Args:
            data: Return data (order_id, product, reason)
            
        Returns:
            Return authorization
        """
        # Generate return authorization (mock)
        rma_number = f'RMA-{random.randint(10000, 99999)}'
        
        return_data = {
            'rma_number': rma_number,
            'order_id': data.get('order_id', 'N/A'),
            'product': data.get('product', 'Product'),
            'reason': data.get('reason', 'Customer request'),
            'return_label': f'https://returns.example.com/{rma_number}',
            'instructions': 'Print the return label and attach it to the package. Drop off at any shipping location within 30 days.'
        }
        
        return {
            'success': True,
            'message': f'Return authorized! RMA Number: {rma_number}. Instructions sent to your email.',
            'return_data': return_data
        }
