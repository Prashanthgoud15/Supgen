# SupportGenie - Quick Setup Guide

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for email notifications)
ADMIN_EMAIL=goudprashanth691@gmail.com
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
```

**Note:** Email notifications will work in "mock mode" without SMTP credentials (emails will be logged to console).

### 3. Initialize Database

The database will be created automatically on first run. To reset:

```bash
# Delete existing database
rm -rf database/supportgenie.db

# Run the app (database will be recreated)
python app.py
```

### 4. Run the Application

```bash
python app.py
```

The app will be available at:
- **Landing Page:** http://localhost:5000
- **Admin Dashboard:** http://localhost:5000/admin
- **Customer Chat:** http://localhost:5000/support

---

## 🌐 Multi-Language Support

### How to Use:
1. Click the language selector (flag icon) in the header
2. Choose: English 🇬🇧, Hindi 🇮🇳, or Telugu 🇮🇳
3. Page reloads with selected language
4. Preference is saved in browser

### Supported Languages:
- **English (en)** - Default
- **Hindi (hi)** - हिंदी
- **Telugu (te)** - తెలుగు

---

## 📧 Email Notifications Setup

### For Gmail:

1. **Enable 2-Step Verification:**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and generate password
   - Copy the 16-character password

3. **Update .env:**
   ```bash
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # App password from step 2
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   ```

### For Other Email Providers:

Update SMTP settings in `.env` according to your provider:
- **Outlook:** smtp.office365.com:587
- **Yahoo:** smtp.mail.yahoo.com:587
- **SendGrid:** smtp.sendgrid.net:587

---

## 🎤 Voice Input

### Browser Support:
- ✅ Chrome (Recommended)
- ✅ Edge
- ✅ Safari
- ⚠️ Firefox (Limited)

### How to Use:
1. Click microphone button in customer chat
2. Allow microphone access when prompted
3. Speak your message
4. Text appears automatically

### Troubleshooting:
- **No microphone button?** Browser doesn't support Web Speech API
- **Permission denied?** Check browser settings → Site permissions
- **Not working?** Try Chrome or Edge

---

## 🗑️ Document Management

### Upload Documents:
1. Go to Admin Dashboard
2. Click "📄 Upload Document"
3. Drag & drop or browse for file
4. Supported formats: PDF, TXT, DOCX, XLSX, XLS, CSV, JSON, MD, XML

### Delete Documents:
1. Find document in Knowledge Base section
2. Click trash icon (🗑️)
3. Confirm deletion
4. Document is soft-deleted (can be restored from database if needed)

---

## 📞 Call Request Feature

### For Customers:
1. Click "📞 Request Call" in chat
2. Enter phone number and preferred time
3. Submit request

### For Admin:
- Email notification sent to: goudprashanth691@gmail.com
- Manager contact: 7842432439
- Contains customer details and callback time

---

## 🎫 Support Tickets

### How It Works:
1. Customer clicks "🎫 Create Ticket"
2. AI asks for confirmation
3. Customer describes issue and selects priority
4. Ticket created with unique ID

### Admin Receives:
- Email notification with:
  - Ticket ID
  - Customer information
  - Full conversation history
  - Priority level (Low/Medium/High)

---

## 🧪 Testing

### Test Multi-Language:
```bash
# Start app
python app.py

# Open browser
# 1. Go to http://localhost:5000/support
# 2. Change language to Hindi or Telugu
# 3. Start conversation
# 4. AI responds in selected language
```

### Test Voice Input:
```bash
# 1. Go to customer chat
# 2. Click microphone button
# 3. Say "I need help with my order"
# 4. Text should appear in input field
```

### Test Email Notifications:
```bash
# 1. Configure SMTP in .env
# 2. Create a support ticket
# 3. Check email at goudprashanth691@gmail.com
```

---

## 🐛 Troubleshooting

### Database Errors:
```bash
# Reset database
rm -rf database/supportgenie.db
python app.py
```

### Import Errors:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Email Not Sending:
- Check SMTP credentials in `.env`
- Verify app password (not regular password)
- Check console for error messages
- Emails will be logged even if SMTP fails

### Voice Input Not Working:
- Use Chrome or Edge browser
- Allow microphone permissions
- Check browser console for errors

---

## 📝 Environment Variables Reference

```bash
# Flask
FLASK_DEBUG=True
PORT=5000

# Database
DATABASE_PATH=database/supportgenie.db

# File Upload
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE_MB=10

# Google Gemini
GEMINI_API_KEY=your_key_here

# Email (Optional)
ADMIN_EMAIL=goudprashanth691@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com

# Manager Contact
MANAGER_PHONE=7842432439
```

---

## 🎉 You're All Set!

Your enhanced SupportGenie is ready to provide next-level AI customer support with:
- 🌐 Multi-language support
- 🎤 Voice input
- 📧 Email notifications
- 🗑️ Document management
- 📞 Call requests
- 🎫 Smart ticketing

Enjoy! 🚀
