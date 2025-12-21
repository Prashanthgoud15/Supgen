"""
Database Migration Script
Adds missing columns to existing SupportGenie database
"""

import sqlite3
import os

def migrate_database():
    """Add missing columns to existing database"""
    db_path = 'database/supportgenie.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found. It will be created on first run.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if language column exists in conversations table
        cursor.execute("PRAGMA table_info(conversations)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'language' not in columns:
            print("Adding 'language' column to conversations table...")
            cursor.execute("ALTER TABLE conversations ADD COLUMN language TEXT DEFAULT 'en'")
            print("✅ Added 'language' column")
        else:
            print("✅ 'language' column already exists")
        
        # Check if deleted_at column exists in documents table
        cursor.execute("PRAGMA table_info(documents)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'deleted_at' not in columns:
            print("Adding 'deleted_at' column to documents table...")
            cursor.execute("ALTER TABLE documents ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL")
            print("✅ Added 'deleted_at' column")
        else:
            print("✅ 'deleted_at' column already exists")
        
        conn.commit()
        print("\n🎉 Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting database migration...\n")
    migrate_database()
