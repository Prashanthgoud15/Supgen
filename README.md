# 🤖 SupportGenie - AI-Powered Customer Support System

**Autonomous multi-agent customer support platform built for MSMEs**

SupportGenie is a production-ready AI customer support system featuring intelligent document processing, context-aware conversations, and autonomous action execution. Built with Google Gemini AI for a hackathon.

![SupportGenie](https://img.shields.io/badge/AI-Powered-purple) ![Flask](https://img.shields.io/badge/Flask-3.0-blue) ![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-orange)

## ✨ Features

### Multi-Agent Architecture
- **Document Agent**: Processes PDFs and structures knowledge automatically
- **Chat Agent**: Handles customer conversations with context awareness
- **Action Agent**: Executes autonomous actions (tickets, returns, orders)

### Admin Portal
- 📊 Real-time analytics dashboard
- 📚 Document management and upload
- 💬 Conversation monitoring
- 📈 Performance metrics

### Customer Portal
- 💬 Natural AI chat interface
- ⚡ Instant responses (< 3 seconds)
- 🎯 Intent detection and action execution
- 📱 Mobile-responsive design

## 🏗️ Architecture

```
┌─────────────────┐
│  Frontend (HTML, CSS, JS)              │
│  - Landing Page                        │
│  - Admin Dashboard                     │
│  - Customer Chat                       │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Flask Backend                         │
│  - REST API                            │
│  - Request Routing                     │
└─────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────┐   ┌─────┐
│Gemini│   │SQLite│
│  AI  │   │  DB  │
└─────┘   └─────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API Key
- pip

### Installation

1. **Clone and navigate to directory**
```bash
cd supportgenie
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
copy .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

5. **Populate demo data (optional)**
```bash
python demo_data.py
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
- **Landing Page**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5000/admin
- **Customer Support**: http://localhost:5000/support

## 📁 Project Structure

```
supportgenie/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── demo_data.py               # Demo data population script
├── Dockerfile                 # Docker configuration
│
├── agents/                    # AI Agents
│   ├── document_agent.py      # PDF processing & structuring
│   ├── chat_agent.py          # Conversation handling
│   └── action_agent.py        # Autonomous actions
│
├── services/                  # Core Services
│   ├── database.py            # SQLite operations
│   └── gemini_service.py      # Gemini AI integration
│
├── static/                    # Frontend
│   ├── index.html             # Landing page
│   ├── admin.html             # Admin dashboard
│   ├── customer.html          # Customer chat
│   ├── css/
│   │   └── style.css          # Global styles
│   └── js/
│       ├── admin.js           # Admin logic
│       └── customer.js        # Customer chat logic
│
├── database/                  # SQLite database
│   └── supportgenie.db        # Auto-created
│
└── uploads/                   # PDF storage
    └── (uploaded files)
```

## 🎮 How to Use

### For Admins

1. **Upload Documents**
   - Click "Upload Document" button
   - Drag & drop or select PDF files
   - AI automatically processes and structures content

2. **Monitor Conversations**
   - View all customer conversations
   - Filter by status (Active/Resolved)
   - Click to view full conversation history

3. **Track Analytics**
   - Today's conversation count
   - Total documents in knowledge base
   - Active chat sessions
   - Average response time

### For Customers

1. **Start Chat**
   - Enter your name (email optional)
   - Click "Start Chat"

2. **Ask Questions**
   - Type naturally - no specific format needed
   - AI responds using knowledge base
   - Get instant, accurate answers

3. **Execute Actions**
   - Click quick action buttons OR
   - Ask naturally (e.g., "I want to return my order")
   - Confirm action details
   - Receive instant confirmation

## 🌐 Deployment to Google Cloud Run

### Prerequisites
- Google Cloud account
- gcloud CLI installed
- Docker installed

### Deployment Steps

1. **Authenticate with Google Cloud**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Build and push Docker image**
```bash
# Build the image
docker build -t gcr.io/YOUR_PROJECT_ID/supportgenie .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/supportgenie
```

3. **Deploy to Cloud Run**
```bash
gcloud run deploy supportgenie \
  --image gcr.io/YOUR_PROJECT_ID/supportgenie \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key_here
```

4. **Access your deployed app**
Cloud Run will provide a URL like: `https://supportgenie-xxx-uc.a.run.app`

### Alternative: One-Command Deploy

```bash
gcloud run deploy supportgenie \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key_here
```

## 🎯 Demo Script (For Hackathon Presentation)

### 1. Landing Page (30 seconds)
- Show hero section highlighting multi-agent AI
- Explain the problem: MSMEs need enterprise-grade support
- Point out the three AI agents

### 2. Admin Dashboard (2 minutes)
- Show analytics cards with live data
- Demo document upload (drag & drop a sample PDF)
- Show document processing (AI structuring)
- Browse conversations list
- Open a conversation to show full history

### 3. Customer Chat (2 minutes)
- Open customer portal in new window
- Start conversation with name
- Ask product question → AI responds from documents
- Request return → Show action execution
- Create support ticket → Show autonomous escalation

### 4. Technical Deep Dive (1 minute)
- Explain architecture: 3 agents working together
- Show tech stack: Flask + Gemini + SQLite
- Highlight simplicity (no complex vector DB needed)
- Mention Cloud Run ready deployment

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | **Required** |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `DATABASE_PATH` | SQLite database path | `database/supportgenie.db` |
| `UPLOAD_FOLDER` | PDF upload directory | `uploads` |
| `MAX_FILE_SIZE_MB` | Max PDF size | `10` |
| `PORT` | Server port | `5000` |

## 🧪 Testing Checklist

- [x] Upload valid PDF → Success
- [x] Upload invalid file → Error message
- [x] Send customer message → AI response
- [x] Execute action → Confirmation
- [x] Admin dashboard loads
- [x] Analytics update
- [x] Conversations display
- [x] Mobile responsive UI

## 🎨 Tech Stack

**Backend**
- Python 3.11
- Flask 3.0
- Google Gemini AI (1.5-flash)
- SQLite
- PyPDF2

**Frontend**
- HTML5
- CSS3 (Tailwind CSS)
- Vanilla JavaScript
- No frameworks (lightweight!)

**Deployment**
- Docker
- Google Cloud Run
- Gunicorn

## 📊 Database Schema

### documents
```sql
id, filename, original_content, structured_content, uploaded_at
```

### conversations
```sql
id, customer_name, customer_email, started_at, status, satisfaction_rating
```

### messages
```sql
id, conversation_id, sender, message, timestamp, source_document_id
```

### actions
```sql
id, conversation_id, action_type, action_data, status, created_at
```

## 🚧 Known Limitations

- Demo version: Some actions are mocked (order tracking, returns)
- Single database: Not optimized for high concurrency
- No authentication: Demo purposes only
- File upload: PDFs only, 10MB max

## 🔮 Future Enhancements

- [ ] Admin authentication & user management
- [ ] WebSocket for real-time updates
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Analytics export (CSV, PDF)
- [ ] Integration with external ticketing systems
- [ ] Email automation
- [ ] Customer satisfaction surveys

## 📝 License

Built for hackathon purposes. Free to use and modify.

## 👥 Team

Built with ❤️ for the hackathon by a passionate developer leveraging the power of AI to revolutionize customer support for small businesses.

## 🤝 Support

For issues or questions:
1. Check this README
2. Review code comments
3. Test with demo data

---

**🤖 SupportGenie - Because every business deserves AI-powered support**

*Built with Google Gemini AI | Powered by Multi-Agent Architecture*
#   S u p p g e n  
 #   S u p g e n  
 