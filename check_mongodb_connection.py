#!/usr/bin/env python
"""
MongoDB Connection Checker for EB Calculator
This script verifies your MongoDB localhost connection and database setup
"""
import sys
import os
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_mongodb_service():
    """Check if MongoDB service is running"""
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=2000)
        # Force connection
        client.server_info()
        print("✓ MongoDB service is running on localhost:27017")
        return True, client
    except Exception as e:
        print(f"✗ MongoDB service check failed: {e}")
        print("\nTo start MongoDB:")
        print("Windows: net start MongoDB (or start MongoDB service)")
        print("macOS: brew services start mongodb-community")
        print("Linux: sudo systemctl start mongod")
        return False, None

def check_database_connection():
    """Check database connection and collections"""
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017)
        db = client['eb_calculator_db']
        
        # List collections
        collections = db.list_collection_names()
        print(f"✓ Connected to database 'eb_calculator_db'")
        print(f"  Collections found: {collections if collections else 'None (new database)'}")
        
        # Test write operation
        test_collection = db['connection_test']
        test_doc = {
            'test': True,
            'timestamp': datetime.now(),
            'message': 'MongoDB connection test successful'
        }
        result = test_collection.insert_one(test_doc)
        print(f"✓ Write test successful (ID: {result.inserted_id})")
        
        # Clean up test document
        test_collection.delete_one({'_id': result.inserted_id})
        print("✓ Read/Delete test successful")
        
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def check_django_mongoengine():
    """Check Django-MongoEngine integration"""
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
        import django
        django.setup()
        
        print("✓ Django setup successful")
        
        # Test MongoEngine models
        from bills.models import User, DailyUsage
        print("✓ MongoEngine models imported successfully")
        
        # Test model operations
        user_count = User.objects.count()
        usage_count = DailyUsage.objects.count()
        print(f"✓ Model queries successful")
        print(f"  Users in database: {user_count}")
        print(f"  Usage records in database: {usage_count}")
        
        return True
    except Exception as e:
        print(f"✗ Django-MongoEngine integration failed: {e}")
        return False

def show_database_stats():
    """Show database statistics"""
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017)
        db = client['eb_calculator_db']
        
        print("\n📊 Database Statistics:")
        print("=" * 50)
        
        collections = db.list_collection_names()
        for collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({})
            print(f"  {collection_name}: {count} documents")
            
            # Show sample document structure
            if count > 0:
                sample = collection.find_one()
                if sample:
                    keys = list(sample.keys())
                    print(f"    Sample fields: {keys[:5]}{'...' if len(keys) > 5 else ''}")
        
        if not collections:
            print("  No collections found (new database)")
            
    except Exception as e:
        print(f"Error getting database stats: {e}")

def main():
    """Main connection check function"""
    print("🔍 MongoDB Connection Checker for EB Calculator")
    print("=" * 60)
    
    # Step 1: Check MongoDB service
    print("\n1. Checking MongoDB service...")
    service_ok, client = check_mongodb_service()
    
    if not service_ok:
        print("\n❌ MongoDB service is not running. Please start MongoDB first.")
        return False
    
    # Step 2: Check database connection
    print("\n2. Checking database connection...")
    db_ok = check_database_connection()
    
    if not db_ok:
        print("\n❌ Database connection failed.")
        return False
    
    # Step 3: Check Django integration
    print("\n3. Checking Django-MongoEngine integration...")
    django_ok = check_django_mongoengine()
    
    if not django_ok:
        print("\n❌ Django integration failed.")
        return False
    
    # Step 4: Show database stats
    show_database_stats()
    
    print("\n✅ All checks passed! Your MongoDB connection is ready.")
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://localhost:8000")
    print("3. Use the EB Calculator with MongoDB storage!")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
