"""
Demo Data Population Script
Creates sample data for impressive hackathon demo
"""

from services.database import Database
from services.gemini_service import GeminiService
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

def create_demo_data():
    """Create demo conversations and data"""
    
    db = Database('database/supportgenie.db')
    
    print("🤖 Creating demo data for SupportGenie...")
    
    # Sample conversations
    conversations_data = [
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.j@email.com',
            'messages': [
                ('customer', 'Hi, my wireless headphones won\'t connect to my phone'),
                ('ai', 'Hello Sarah! 👋 I can help you with that. Have you tried turning Bluetooth off and on again on your phone?'),
                ('customer', 'Yes, I tried that but it\'s still not working'),
                ('ai', 'Let\'s try resetting the headphones. Hold the power button for 10 seconds until you see a red light. Then try pairing again. Does that work?'),
                ('customer', 'It worked! Thanks so much!'),
                ('ai', 'Great! I\'m happy I could help. Is there anything else you need? 😊')
            ],
            'status': 'resolved'
        },
        {
            'name': 'Michael Chen',
            'email': 'mchen@company.com',
            'messages': [
                ('customer', 'I need to return my SmartPhone Pro, the screen is cracked'),
                ('ai', 'I\'m sorry to hear that! 😔 I can help you with a return. Can you provide your order ID?'),
                ('customer', 'It\'s ORD-7453'),
                ('ai', 'Thank you! I\'ve created a return authorization for you. RMA Number: RMA-78345. You\'ll receive a return shipping label via email within the next hour.')
            ],
            'status': 'active'
        },
        {
            'name': 'Emily Rodriguez',
            'email': 'emily.r@gmail.com',
            'messages': [
                ('customer', 'What\'s the warranty on the Laptop X1?'),
                ('ai', 'The Laptop X1 comes with a 2-year manufacturer warranty covering hardware defects. This includes the screen, keyboard, battery, and internal components. Would you like more details? 😊'),
                ('customer', 'Does it cover accidental damage?'),
                ('ai', 'The standard warranty doesn\'t cover accidental damage, but you can purchase our extended protection plan within 30 days of purchase. Would you like information about that?')
            ],
            'status': 'active'
        },
        {
            'name': 'David Kim',
            'email': None,
            'messages': [
                ('customer', 'How do I check my order status?'),
                ('ai', 'I can help you check your order status! 📦 Please provide your order ID, and I\'ll look it up for you.'),
                ('customer', 'ORD-2891'),
                ('ai', 'Your order ORD-2891 is currently out for delivery! Expected arrival: Today by 8 PM. You can track it with tracking number TRK123456789.')
            ],
            'status': 'resolved'
        },
        {
            'name': 'Lisa Anderson',
            'email': 'l.anderson@work.com',
            'messages': [
                ('customer', 'The touch screen on my phone stopped working'),
                ('ai', 'I\'m sorry you\'re experiencing that issue! Let\'s troubleshoot this. First, try restarting your phone. If that doesn\'t work, we may need to escalate this for a repair or replacement.'),
                ('customer', 'I restarted it multiple times, still not working'),
                ('ai', 'I understand this is frustrating. I\'ve created a support ticket (TKT-39482) for you. Our technical team will contact you within 24 hours to arrange a repair or replacement. Is there anything else I can help with?')
            ],
            'status': 'escalated'
        },
        {
            'name': 'James Taylor',
            'email': 'jtaylor@email.com',
            'messages': [
                ('customer', 'Do you have SmartPhone Pro in blue color?'),
                ('ai', 'Yes! The SmartPhone Pro is available in Midnight Blue, Silver, and Black. The Midnight Blue is very popular! 💙 Would you like to place an order?'),
                ('customer', 'What\'s the price?'),
                ('ai', 'The SmartPhone Pro is $699 for the 128GB model and $799 for the 256GB model. We also have a promotion right now: free wireless charger with purchase! 🎁')
            ],
            'status': 'active'
        }
    ]
    
    # Create conversations with time offsets
    for i, conv_data in enumerate(conversations_data):
        try:
            # Create conversation
            conv_id = db.create_conversation(
                customer_name=conv_data['name'],
                customer_email=conv_data['email']
            )
            
            # Add messages with timestamps
            for msg in conv_data['messages']:
                db.save_message(
                    conversation_id=conv_id,
                    sender=msg[0],
                    message=msg[1]
                )
            
            # Update status if needed
            if conv_data['status'] != 'active':
                db.update_conversation_status(conv_id, conv_data['status'])
            
            print(f"✅ Created conversation for {conv_data['name']}")
        
        except Exception as e:
            print(f"❌ Error creating conversation for {conv_data['name']}: {e}")
    
    print("\n📊 Demo data creation complete!")
    print(f"Total conversations: {len(conversations_data)}")
    print("\n🚀 You can now run the application and see the demo data in the admin dashboard!")

if __name__ == '__main__':
    create_demo_data()
