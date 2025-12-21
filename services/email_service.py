"""
Email Service for SupportGenie
Handles email notifications for support tickets and call requests
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional


class EmailService:
    """Service for sending email notifications"""
    
    def __init__(self):
        """Initialize Email Service with SMTP configuration"""
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.admin_email = os.getenv('ADMIN_EMAIL', 'goudprashanth691@gmail.com')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_user)
        
        # Check if email is configured
        self.is_configured = bool(self.smtp_user and self.smtp_password)
        
        if not self.is_configured:
            print("⚠️ Email service not configured. Set SMTP_USER and SMTP_PASSWORD in .env")
    
    def send_email(self, to_email: str, subject: str, body_html: str, body_text: str = None) -> bool:
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML body content
            body_text: Plain text body (optional)
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_configured:
            print(f"📧 [MOCK] Email would be sent to {to_email}: {subject}")
            return True  # Return True for development without SMTP
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            if body_text:
                part1 = MIMEText(body_text, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(body_html, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def send_support_ticket_notification(self, ticket_data: Dict, conversation_history: List[Dict]) -> bool:
        """
        Send support ticket notification to admin
        
        Args:
            ticket_data: Ticket information
            conversation_history: List of conversation messages
            
        Returns:
            True if sent successfully
        """
        ticket_id = ticket_data.get('ticket_id', 'N/A')
        customer_name = ticket_data.get('customer_name', 'Unknown')
        customer_email = ticket_data.get('customer_email', 'Not provided')
        issue_summary = ticket_data.get('issue_summary', 'No summary provided')
        priority = ticket_data.get('priority', 'medium').upper()
        
        # Build conversation history HTML
        history_html = ""
        for msg in conversation_history[-10:]:  # Last 10 messages
            sender = msg.get('sender', 'unknown')
            message = msg.get('message', '')
            timestamp = msg.get('timestamp', '')
            
            if sender == 'customer':
                history_html += f"""
                <div style="margin: 10px 0; padding: 10px; background: #f3f4f6; border-radius: 8px;">
                    <strong style="color: #6366f1;">Customer:</strong> {message}
                    <br><small style="color: #6b7280;">{timestamp}</small>
                </div>
                """
            else:
                history_html += f"""
                <div style="margin: 10px 0; padding: 10px; background: #ede9fe; border-radius: 8px;">
                    <strong style="color: #7c3aed;">AI Assistant:</strong> {message}
                    <br><small style="color: #6b7280;">{timestamp}</small>
                </div>
                """
        
        # Priority color
        priority_colors = {
            'LOW': '#10b981',
            'MEDIUM': '#f59e0b',
            'HIGH': '#ef4444'
        }
        priority_color = priority_colors.get(priority, '#6b7280')
        
        # Email subject
        subject = f"🎫 New Support Ticket - {ticket_id}"
        
        # HTML body
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; color: #6b7280; border-radius: 0 0 10px 10px; }}
                .badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; color: white; font-weight: bold; }}
                .info-box {{ background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">🤖 SupportGenie</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">New Support Ticket Created</p>
                </div>
                
                <div class="content">
                    <h2 style="color: #1f2937; margin-top: 0;">Ticket Details</h2>
                    
                    <div class="info-box">
                        <p><strong>Ticket ID:</strong> {ticket_id}</p>
                        <p><strong>Priority:</strong> <span class="badge" style="background: {priority_color};">{priority}</span></p>
                        <p><strong>Created:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <h3 style="color: #1f2937;">Customer Information</h3>
                    <div class="info-box">
                        <p><strong>Name:</strong> {customer_name}</p>
                        <p><strong>Email:</strong> {customer_email}</p>
                    </div>
                    
                    <h3 style="color: #1f2937;">Issue Summary</h3>
                    <div class="info-box">
                        <p>{issue_summary}</p>
                    </div>
                    
                    <h3 style="color: #1f2937;">Conversation History</h3>
                    {history_html}
                    
                    <div style="margin-top: 30px; padding: 20px; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 4px;">
                        <p style="margin: 0;"><strong>⚡ Action Required:</strong> Please review this ticket and respond to the customer within 24 hours.</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This is an automated notification from SupportGenie AI Customer Support System</p>
                    <p style="font-size: 12px; margin-top: 10px;">Powered by Google Gemini AI</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        body_text = f"""
        New Support Ticket Created
        
        Ticket ID: {ticket_id}
        Priority: {priority}
        
        Customer: {customer_name}
        Email: {customer_email}
        
        Issue: {issue_summary}
        
        Please review this ticket and respond within 24 hours.
        """
        
        return self.send_email(self.admin_email, subject, body_html, body_text)
    
    def send_call_request_notification(self, customer_data: Dict) -> bool:
        """
        Send call request notification to admin
        
        Args:
            customer_data: Customer information and callback details
            
        Returns:
            True if sent successfully
        """
        customer_name = customer_data.get('customer_name', 'Unknown')
        customer_email = customer_data.get('customer_email', 'Not provided')
        phone_number = customer_data.get('phone_number', 'Not provided')
        preferred_time = customer_data.get('preferred_time', 'ASAP')
        reason = customer_data.get('reason', 'Not specified')
        
        subject = f"📞 Call Request from {customer_name}"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; color: #6b7280; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                .urgent {{ background: #fee2e2; border-left: 4px solid #ef4444; padding: 15px; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">📞 Call Request</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Customer requesting callback</p>
                </div>
                
                <div class="content">
                    <h2 style="color: #1f2937; margin-top: 0;">Customer Details</h2>
                    
                    <div class="info-box">
                        <p><strong>Name:</strong> {customer_name}</p>
                        <p><strong>Email:</strong> {customer_email}</p>
                        <p><strong>Phone:</strong> {phone_number}</p>
                        <p><strong>Preferred Time:</strong> {preferred_time}</p>
                    </div>
                    
                    <h3 style="color: #1f2937;">Reason for Call</h3>
                    <div class="info-box">
                        <p>{reason}</p>
                    </div>
                    
                    <div class="urgent">
                        <p style="margin: 0;"><strong>⚡ Action Required:</strong> Please contact the customer at the preferred time.</p>
                        <p style="margin: 10px 0 0 0;">Manager Contact: 7842432439</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This is an automated notification from SupportGenie</p>
                    <p style="font-size: 12px; margin-top: 10px;">Request received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        body_text = f"""
        Call Request from Customer
        
        Name: {customer_name}
        Email: {customer_email}
        Phone: {phone_number}
        Preferred Time: {preferred_time}
        
        Reason: {reason}
        
        Please contact the customer as soon as possible.
        Manager Contact: 7842432439
        """
        
        return self.send_email(self.admin_email, subject, body_html, body_text)
