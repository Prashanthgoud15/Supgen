"""
SupportGenie - AI-Powered Customer Support System
Main Flask Application
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

# Import services and agents
from services.database import Database
from services.gemini_service import GeminiService
from services.translation_service import TranslationService
from services.email_service import EmailService
from agents.document_agent import DocumentAgent
from agents.chat_agent import ChatAgent
from agents.action_agent import ActionAgent

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE_MB', 10)) * 1024 * 1024  # MB to bytes
app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', 'database/supportgenie.db')

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
db = Database(app.config['DATABASE_PATH'])
gemini_service = GeminiService()
translation_service = TranslationService()
email_service = EmailService()

# Initialize agents
document_agent = DocumentAgent(gemini_service, db)
chat_agent = ChatAgent(gemini_service, db)
action_agent = ActionAgent(gemini_service, db)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'csv', 'json', 'md', 'xml', 'xlsx', 'xls'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================================
# GENERAL ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve landing page"""
    return send_from_directory('static', 'index.html')

@app.route('/admin')
def admin():
    """Serve admin dashboard"""
    return send_from_directory('static', 'admin.html')

@app.route('/support')
def support():
    """Serve customer chat interface"""
    return send_from_directory('static', 'customer.html')

# Serve static files
@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    return send_from_directory('static/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    return send_from_directory('static/js', filename)


# ============================================================================
# ADMIN API ROUTES
# ============================================================================

@app.route('/api/admin/upload-document', methods=['POST'])
def upload_document():
    """
    Upload and process a document (PDF, TXT, DOCX, XLSX, XLS, CSV, JSON, MD, XML)
    Expected: multipart/form-data with 'document' file field
    """
    try:
        # Check if file is in request
        if 'document' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['document']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Supported file formats: PDF, TXT, DOCX, XLSX, XLS, CSV, JSON, MD, XML'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process with Document Agent
        result = document_agent.process_document(filepath)
        
        if result['success']:
            return jsonify({
                'success': True,
                'document_id': result['document_id'],
                'filename': result['filename'],
                'message': 'Document uploaded and processed successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to process document')
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/admin/documents', methods=['GET'])
def get_documents():
    """Get all uploaded documents"""
    try:
        documents = document_agent.get_all_documents()
        return jsonify({
            'success': True,
            'documents': documents
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/admin/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations"""
    try:
        conversations = db.get_all_conversations()
        return jsonify({
            'success': True,
            'conversations': conversations
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/admin/conversation/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get specific conversation with all messages"""
    try:
        conversation = db.get_conversation_by_id(conversation_id)
        
        if not conversation:
            return jsonify({
                'success': False,
                'error': 'Conversation not found'
            }), 404
        
        messages = db.get_conversation_messages(conversation_id)
        
        return jsonify({
            'success': True,
            'conversation': conversation,
            'messages': messages
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/admin/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data for dashboard"""
    try:
        analytics = db.get_analytics()
        return jsonify({
            'success': True,
            'analytics': analytics
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/admin/delete-document/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    """Delete a document (soft delete)"""
    try:
        success = db.delete_document(document_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Document deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Document not found or already deleted'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/translations/<language>', methods=['GET'])
def get_translations(language):
    """Get UI translations for a specific language"""
    try:
        translations = translation_service.get_ui_translations(language)
        return jsonify({
            'success': True,
            'translations': translations,
            'language': language
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


# ============================================================================
# CUSTOMER API ROUTES
# ============================================================================

@app.route('/api/customer/start-conversation', methods=['POST'])
def start_conversation():
    """
    Start a new customer conversation
    Expected JSON: {customer_name: str, customer_email: str (optional), language: str (optional)}
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'customer_name' not in data:
            return jsonify({
                'success': False,
                'error': 'customer_name is required'
            }), 400
        
        customer_name = data['customer_name']
        customer_email = data.get('customer_email', None)
        language = data.get('language', 'en')  # Default to English
        
        # Create conversation with language
        conversation_id = db.create_conversation(customer_name, customer_email, language)
        
        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'language': language,
            'message': 'Conversation started successfully'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/customer/send-message', methods=['POST'])
def send_message():
    """
    Send a customer message and get AI response
    Expected JSON: {conversation_id: int, message: str}
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'conversation_id' not in data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'conversation_id and message are required'
            }), 400
        
        conversation_id = data['conversation_id']
        user_message = data['message']
        
        # Handle message with Chat Agent
        chat_result = chat_agent.handle_message(conversation_id, user_message)
        
        if not chat_result['success']:
            return jsonify(chat_result), 400
        
        # Detect intent for potential actions
        intent_result = gemini_service.detect_intent(user_message)
        
        action_taken = None
        
        # Execute action if needed (and intent confidence is not low)
        if intent_result['intent'] != 'general_query' and intent_result['confidence'] != 'low':
            action_data = {
                'user_message': user_message,
                'intent': intent_result['intent'],
                'entities': intent_result['entities']
            }
            
            action_result = action_agent.execute_action(
                conversation_id=conversation_id,
                action_type=intent_result['intent'],
                action_data=action_data
            )
            
            if action_result['success']:
                action_taken = {
                    'type': intent_result['intent'],
                    'result': action_result
                }
        
        return jsonify({
            'success': True,
            'ai_response': chat_result['response'],
            'source_documents': chat_result.get('source_documents', []),
            'action_taken': action_taken
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/customer/conversation/<int:conversation_id>', methods=['GET'])
def get_customer_conversation(conversation_id):
    """Get conversation messages for customer"""
    try:
        messages = db.get_conversation_messages(conversation_id)
        
        return jsonify({
            'success': True,
            'messages': messages
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/customer/execute-action', methods=['POST'])
def execute_action():
    """
    Execute a specific customer action
    Expected JSON: {conversation_id: int, action_type: str, action_data: dict}
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'conversation_id' not in data or 'action_type' not in data:
            return jsonify({
                'success': False,
                'error': 'conversation_id and action_type are required'
            }), 400
        
        conversation_id = data['conversation_id']
        action_type = data['action_type']
        action_data = data.get('action_data', {})
        
        # Execute action
        result = action_agent.execute_action(conversation_id, action_type, action_data)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/customer/request-call', methods=['POST'])
def request_call():
    """
    Request a callback from support team
    Expected JSON: {conversation_id: int, customer_name: str, customer_email: str, 
                    phone_number: str, preferred_time: str, reason: str}
    """
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['customer_name', 'phone_number']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        # Send email notification
        email_sent = email_service.send_call_request_notification(data)
        
        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Call request submitted successfully! Our team will contact you soon.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to submit call request. Please try again.'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("=" * 60)
    print("🤖 SupportGenie - AI Customer Support System")
    print("=" * 60)
    print(f"Server running on: http://localhost:{port}")
    print(f"Admin Dashboard: http://localhost:{port}/admin")
    print(f"Customer Support: http://localhost:{port}/support")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
