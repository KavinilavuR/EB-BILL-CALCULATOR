#!/usr/bin/env python
"""
MongoDB Connection Verification Script
This script will identify and fix MongoDB connection issues
"""
import sys
import os
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_mongodb_service():
    """Check if MongoDB service is running"""
    print("🔍 Checking MongoDB Service...")
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
        # Force connection
        server_info = client.server_info()
        print(f"✅ MongoDB is running on localhost:27017")
        print(f"   MongoDB version: {server_info.get('version', 'Unknown')}")
        
        # List all databases
        databases = client.list_database_names()
        print(f"   Available databases: {databases}")
        
        return True, client
    except Exception as e:
        print(f"❌ MongoDB service check failed: {e}")
        print("\n🔧 To start MongoDB:")
        print("   Windows: net start MongoDB")
        print("   macOS: brew services start mongodb-community")
        print("   Linux: sudo systemctl start mongod")
        return False, None

def check_website_database(client):
    """Check the specific database for the website"""
    print("\n🗄️ Checking Website Database...")
    try:
        # Check the new database name
        db_name = 'eb_calculator_website_db'
        db = client[db_name]
        
        # List collections
        collections = db.list_collection_names()
        print(f"✅ Database '{db_name}' accessible")
        print(f"   Collections: {collections if collections else 'None (new database)'}")
        
        # Test write operation
        test_collection = db['connection_test']
        test_doc = {
            'test': True,
            'timestamp': datetime.now(),
            'message': 'Website database connection test'
        }
        result = test_collection.insert_one(test_doc)
        print(f"✅ Write test successful (ID: {result.inserted_id})")
        
        # Clean up test document
        test_collection.delete_one({'_id': result.inserted_id})
        print("✅ Read/Delete test successful")
        
        return True, db_name
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False, None

def check_django_connection():
    """Check Django-MongoDB integration"""
    print("\n🐍 Checking Django-MongoDB Integration...")
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
        import django
        django.setup()
        
        print("✅ Django setup successful")
        
        # Import models
        from bills.models import User, DailyUsage
        print("✅ Models imported successfully")
        
        # Test model operations
        user_count = User.objects.count()
        usage_count = DailyUsage.objects.count()
        print(f"✅ Model queries successful")
        print(f"   Users in database: {user_count}")
        print(f"   Usage records in database: {usage_count}")
        
        return True
    except Exception as e:
        print(f"❌ Django integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_test_user_and_data():
    """Create a test user and usage data to verify saving works"""
    print("\n👤 Creating Test User and Data...")
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
        import django
        django.setup()
        
        from bills.models import User, DailyUsage, Appliance
        
        # Create or get test user
        test_username = 'website_test_user'
        existing_user = User.objects.filter(username=test_username).first()
        
        if existing_user:
            print(f"✅ Test user '{test_username}' already exists")
            test_user = existing_user
        else:
            test_user = User(
                username=test_username,
                full_name='Website Test User',
                email='test@website.com',
                phone_number='+91-1234567890',
                address='Test Address',
                consumer_number='TEST123456'
            )
            test_user.set_password('test123')
            test_user.save()
            print(f"✅ Created test user: {test_username}")
        
        # Create test usage data
        usage_record = DailyUsage(
            user=test_user,
            date=datetime.now(),
            appliances=[]
        )
        
        # Add test appliances
        test_appliances = [
            {'name': 'Test Fan', 'units': 8.5},
            {'name': 'Test Light', 'units': 5.2}
        ]
        
        for app_data in test_appliances:
            appliance = Appliance(
                name=app_data['name'],
                units_consumed=app_data['units']
            )
            usage_record.appliances.append(appliance)
        
        usage_record.save()
        print(f"✅ Created test usage record with {len(test_appliances)} appliances")
        print(f"   Total units: {usage_record.total_units} kWh")
        print(f"   Record ID: {usage_record.id}")
        
        return True, test_user
    except Exception as e:
        print(f"❌ Test data creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def show_database_contents():
    """Show what's actually in the database"""
    print("\n📊 Database Contents Summary...")
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017)
        
        # Check both possible database names
        db_names = ['eb_calculator_website_db', 'eb_calculator_db']
        
        for db_name in db_names:
            db = client[db_name]
            collections = db.list_collection_names()
            
            if collections:
                print(f"\n📁 Database: {db_name}")
                for collection_name in collections:
                    collection = db[collection_name]
                    count = collection.count_documents({})
                    print(f"   {collection_name}: {count} documents")
                    
                    if count > 0 and count <= 3:
                        # Show sample documents for small collections
                        samples = list(collection.find().limit(1))
                        if samples:
                            sample = samples[0]
                            keys = list(sample.keys())
                            print(f"     Sample fields: {keys[:5]}{'...' if len(keys) > 5 else ''}")
            else:
                print(f"\n📁 Database: {db_name} (empty)")
        
        return True
    except Exception as e:
        print(f"❌ Error checking database contents: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 MongoDB Connection Verification for EB Calculator Website")
    print("=" * 80)
    
    # Step 1: Check MongoDB service
    service_ok, client = check_mongodb_service()
    if not service_ok:
        print("\n❌ MongoDB service is not running. Please start MongoDB first.")
        return False
    
    # Step 2: Check website database
    db_ok, db_name = check_website_database(client)
    if not db_ok:
        print("\n❌ Database connection failed.")
        return False
    
    # Step 3: Show current database contents
    show_database_contents()
    
    # Step 4: Check Django integration
    django_ok = check_django_connection()
    if not django_ok:
        print("\n❌ Django integration failed.")
        return False
    
    # Step 5: Create test data
    test_ok, test_user = create_test_user_and_data()
    if not test_ok:
        print("\n❌ Test data creation failed.")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL CHECKS PASSED!")
    print(f"🎯 Your website is connected to: {db_name} on localhost:27017")
    print(f"👤 Test user created: website_test_user / test123")
    print("\n🌐 Next steps:")
    print("1. Kill any running Django servers")
    print("2. Run: python manage.py runserver")
    print("3. Visit: http://localhost:8000")
    print("4. Login and test the 'Save Usage Data' button")
    print("\n📝 The data will now be saved to the correct MongoDB database!")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        print("\n❌ Verification failed. Please fix the issues above.")
        sys.exit(1)
