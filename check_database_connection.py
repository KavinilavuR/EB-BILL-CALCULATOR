#!/usr/bin/env python
"""
Quick check to see which MongoDB database is actually being used
"""
import os
import sys
import django
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
django.setup()

def check_current_database():
    """Check which database is currently connected"""
    print("🔍 Checking Current Database Connection...")
    
    try:
        import pymongo
        from bills.models import User, DailyUsage
        
        # Check direct MongoDB connection
        client = pymongo.MongoClient('localhost', 27017)
        databases = client.list_database_names()
        print(f"📊 Available MongoDB databases: {databases}")
        
        # Check which database Django is using
        from mongoengine.connection import get_db
        current_db = get_db()
        print(f"🎯 Django is connected to database: '{current_db.name}'")
        
        # Check collections in current database
        collections = current_db.list_collection_names()
        print(f"📁 Collections in '{current_db.name}': {collections}")
        
        # Check user count
        user_count = User.objects.count()
        usage_count = DailyUsage.objects.count()
        print(f"👤 Users in current database: {user_count}")
        print(f"📈 Usage records in current database: {usage_count}")
        
        # Show sample data if exists
        if user_count > 0:
            sample_user = User.objects.first()
            print(f"📝 Sample user: {sample_user.username}")
        
        if usage_count > 0:
            sample_usage = DailyUsage.objects.first()
            print(f"📝 Sample usage: {sample_usage.date} - {sample_usage.total_units} kWh")
        
        return current_db.name
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return None

def test_save_operation():
    """Test if save operation works"""
    print("\n🧪 Testing Save Operation...")
    
    try:
        from bills.models import User, DailyUsage, Appliance
        
        # Get or create test user
        test_user = User.objects.filter(username='testuser').first()
        if not test_user:
            print("❌ Test user 'testuser' not found")
            return False
        
        print(f"✅ Found test user: {test_user.username}")
        
        # Create a test usage record
        test_usage = DailyUsage(
            user=test_user,
            date=datetime.now(),
            appliances=[]
        )
        
        # Add test appliance
        test_appliance = Appliance(
            name="Test Save Operation",
            units_consumed=1.5
        )
        test_usage.appliances.append(test_appliance)
        
        # Save to database
        test_usage.save()
        print(f"✅ Save operation successful!")
        print(f"   Record ID: {test_usage.id}")
        print(f"   Total units: {test_usage.total_units} kWh")
        
        # Verify it was saved
        saved_record = DailyUsage.objects.filter(id=test_usage.id).first()
        if saved_record:
            print(f"✅ Record verified in database")
            print(f"   Appliances: {len(saved_record.appliances)}")
            
            # Clean up test record
            saved_record.delete()
            print(f"✅ Test record cleaned up")
            
            return True
        else:
            print(f"❌ Record not found after save")
            return False
            
    except Exception as e:
        print(f"❌ Save operation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Database Connection Check")
    print("=" * 50)
    
    # Check current database
    db_name = check_current_database()
    
    if db_name:
        print(f"\n✅ Your website is connected to: '{db_name}'")
        
        # Test save operation
        save_test = test_save_operation()
        
        print("\n" + "=" * 50)
        if save_test:
            print("🎉 ALL TESTS PASSED!")
            print(f"✅ Database: {db_name}")
            print("✅ Save operation: Working")
            print("\n🌐 Your 'Save Usage Data' button should now work!")
            print("   Try it at: http://127.0.0.1:8000")
        else:
            print("❌ Save operation failed")
    else:
        print("❌ Database connection check failed")

if __name__ == '__main__':
    main()
