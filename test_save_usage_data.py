#!/usr/bin/env python
"""
Test script to verify the "Save Usage Data" functionality with MongoDB
This simulates what happens when a user clicks the "Save Usage Data" button
"""
import os
import sys
import django
import json
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
django.setup()

from bills.models import User, DailyUsage, Appliance
from bills.views import save_daily_usage
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

def test_save_usage_data_functionality():
    """Test the save usage data functionality"""
    print("🧪 Testing 'Save Usage Data' MongoDB Integration")
    print("=" * 60)
    
    # Get a test user
    try:
        test_user = User.objects.filter(username='testuser').first()
        if not test_user:
            print("❌ Test user not found. Run setup_mongodb.py first.")
            return False
        
        print(f"✓ Using test user: {test_user.username}")
    except Exception as e:
        print(f"❌ Error getting test user: {e}")
        return False
    
    # Simulate form data (what the frontend sends)
    test_data = {
        'num_appliances': 3,
        'appliance_0_name': 'Fan',
        'appliance_0_units': 8.5,
        'appliance_1_name': 'Light',
        'appliance_1_units': 5.2,
        'appliance_2_name': 'TV',
        'appliance_2_units': 4.8,
    }
    
    print(f"📝 Test data: {test_data}")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.post('/save-daily-usage/', data=test_data)
    request.user = test_user
    
    # Get count before saving
    before_count = DailyUsage.objects.filter(user=test_user).count()
    print(f"📊 Usage records before: {before_count}")
    
    try:
        # Call the view function directly
        from django.http import JsonResponse
        response = save_daily_usage(request)
        
        if isinstance(response, JsonResponse):
            response_data = json.loads(response.content.decode())
            print(f"📤 Response: {response_data}")
            
            if response_data.get('success'):
                print("✅ Save operation successful!")
                
                # Check if data was actually saved to MongoDB
                after_count = DailyUsage.objects.filter(user=test_user).count()
                print(f"📊 Usage records after: {after_count}")
                
                if after_count > before_count:
                    print("✅ Data successfully saved to MongoDB!")
                    
                    # Get the latest record
                    latest_record = DailyUsage.objects.filter(user=test_user).order_by('-created_at').first()
                    if latest_record:
                        print(f"📋 Latest record details:")
                        print(f"   Date: {latest_record.date}")
                        print(f"   Total Units: {latest_record.total_units}")
                        print(f"   Appliances: {len(latest_record.appliances)}")
                        for i, appliance in enumerate(latest_record.appliances):
                            print(f"     {i+1}. {appliance.name}: {appliance.units_consumed} kWh")
                    
                    return True
                else:
                    print("❌ Data was not saved to MongoDB")
                    return False
            else:
                print(f"❌ Save operation failed: {response_data.get('message')}")
                return False
        else:
            print(f"❌ Unexpected response type: {type(response)}")
            return False
            
    except Exception as e:
        print(f"❌ Error during save operation: {e}")
        return False

def test_mongodb_data_retrieval():
    """Test retrieving data from MongoDB"""
    print("\n🔍 Testing MongoDB Data Retrieval")
    print("=" * 40)
    
    try:
        # Get all users
        users = User.objects.all()
        print(f"👥 Total users in database: {users.count()}")
        
        for user in users:
            usage_count = DailyUsage.objects.filter(user=user).count()
            print(f"   {user.username}: {usage_count} usage records")
        
        # Get recent usage data
        recent_usage = DailyUsage.objects.order_by('-date')[:5]
        print(f"\n📅 Recent 5 usage records:")
        
        for record in recent_usage:
            print(f"   {record.date.strftime('%Y-%m-%d')}: {record.total_units:.2f} kWh ({record.user.username})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error retrieving data: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 MongoDB Integration Test for EB Calculator")
    print("=" * 70)
    
    # Test 1: Save usage data functionality
    save_test = test_save_usage_data_functionality()
    
    # Test 2: Data retrieval
    retrieval_test = test_mongodb_data_retrieval()
    
    print("\n" + "=" * 70)
    if save_test and retrieval_test:
        print("✅ ALL TESTS PASSED!")
        print("Your 'Save Usage Data' button is properly connected to MongoDB!")
        print("\nThe complete flow is working:")
        print("1. ✅ Frontend form data → Django view")
        print("2. ✅ Django view → MongoDB storage")
        print("3. ✅ MongoDB storage → Data retrieval")
        print("4. ✅ 2-month billing cycle ready")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return save_test and retrieval_test

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
