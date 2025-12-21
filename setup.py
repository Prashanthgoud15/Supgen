"""
Quick Setup Script for SupportGenie
Helps configure the application before first run
"""

import os
import sys

def setup_environment():
    """Guide user through environment setup"""
    
    print("=" * 60)
    print("🤖 SupportGenie - Quick Setup")
    print("=" * 60)
    print()
    
    # Check if .env exists
    env_file = '.env'
    
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        response = input("Do you want to reconfigure it? (y/n): ").lower()
        if response != 'y':
            print("\nSetup cancelled. Your existing configuration will be used.")
            return
    
    print("\n📝 Let's set up your environment variables\n")
    
    # Get Gemini API Key
    print("1. Gemini API Key")
    print("   Get your free API key at: https://makersuite.google.com/app/apikey")
    api_key = input("\n   Enter your Gemini API Key: ").strip()
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("\n❌ Valid API key is required!")
        sys.exit(1)
    
    # Create .env file
    env_content = f"""# Google Gemini API Key
GEMINI_API_KEY={api_key}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_PATH=database/supportgenie.db

# Upload Configuration
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE_MB=10
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("\n✅ Environment configured successfully!")
    print("\n" + "=" * 60)
    print("📊 Optional: Create demo data?")
    print("=" * 60)
    print("Demo data includes sample conversations for testing.")
    response = input("Create demo data? (y/n): ").lower()
    
    if response == 'y':
        print("\n🔄 Creating demo data...")
        try:
            import demo_data
            demo_data.create_demo_data()
        except Exception as e:
            print(f"⚠️  Error creating demo data: {e}")
            print("You can run 'python demo_data.py' manually later")
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("\n📖 Next Steps:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Enjoy your AI-powered support system!")
    print("\n🚀 Good luck with your hackathon!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        setup_environment()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)
