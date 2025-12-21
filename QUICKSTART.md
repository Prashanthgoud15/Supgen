# 🚀 Quick Start Guide - SupportGenie

## Fastest Way to Get Started

### 1. Get Your Gemini API Key
Visit: https://makersuite.google.com/app/apikey

### 2. Run Setup Script
```bash
python setup.py
```
This will:
- Ask for your Gemini API key
- Create the .env configuration file
- Optionally create demo data

### 3. Start the Application
```bash
python app.py
```

### 4. Open in Browser
- Landing Page: http://localhost:5000
- Admin Dashboard: http://localhost:5000/admin
- Customer Chat: http://localhost:5000/support

## That's It!

For detailed instructions, see README.md

---

### Troubleshooting

**Problem**: Dependencies not installed
**Solution**: 
```bash
pip install -r requirements.txt
```

**Problem**: Port 5000 already in use
**Solution**: Edit .env and change PORT=5000 to PORT=8000 (or any other port)

**Problem**: Gemini API error
**Solution**: Double-check your API key at .env file

---

### Demo Features to Try

1. **Upload a PDF** in admin dashboard (use any product manual)
2. **Ask questions** in customer chat that relate to the PDF
3. **Request actions** like "I want to return my order"
4. **View analytics** in admin dashboard

---

**Need help?** Check README.md for complete documentation!
