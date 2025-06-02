#!/usr/bin/env python
"""
Test the fixed save_daily_usage functionality
This simulates the exact data format sent by the frontend
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

from bills.models import User, DailyUsage
from bills.views import save_daily_usage
from django.test import RequestFactory
from django.http import JsonResponse

def test_json_format_save():
    """Test saving with the JSON format that frontend sends"""
    print("🧪 Testing Save Usage Data with JSON Format")
    print("=" * 50)
    
    try:
        # Get test user
        test_user = User.objects.filter(username='testuser').first()
        if not test_user:
            print("❌ Test user not found")
            return False
        
        print(f"✓ Using user: {test_user.username}")
        
        # Count before
        before_count = DailyUsage.objects.filter(user=test_user).count()
        print(f"📊 Records before: {before_count}")
        
        # Create the exact JSON format that frontend sends
        test_data = {
            "appliances": [
                {"name": "Ceiling Fan (75W)", "units_consumed": 8.5},
                {"name": "LED Bulb (10W)", "units_consumed": 5.2},
                {"name": "Television (150W)", "units_consumed": 4.8}
            ],
            "notes": ""
        }
        
        print(f"📝 Test data: {json.dumps(test_data, indent=2)}")
        
        # Create mock request with JSON data
        factory = RequestFactory()
        request = factory.post(
            '/add-usage/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        request.user = test_user
        
        # Call the view function
        response = save_daily_usage(request)
        
        if isinstance(response, JsonResponse):
            response_data = json.loads(response.content.decode())
            print(f"📤 Response: {json.dumps(response_data, indent=2)}")
            
            if response_data.get('success'):
                print("✅ Save operation successful!")
                
                # Check if data was saved
                after_count = DailyUsage.objects.filter(user=test_user).count()
                print(f"📊 Records after: {after_count}")
                
                if after_count > before_count:
                    print("✅ Data successfully saved to MongoDB!")
                    
                    # Get the latest record
                    latest_record = DailyUsage.objects.filter(user=test_user).order_by('-date').first()
                    if latest_record:
                        print(f"📋 Latest record details:")
                        print(f"   Date: {latest_record.date}")
                        print(f"   Total Units: {latest_record.total_units} kWh")
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
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_form_data_format():
    """Test saving with form data format (for compatibility)"""
    print("\n🧪 Testing Save Usage Data with Form Data Format")
    print("=" * 50)
    
    try:
        # Get test user
        test_user = User.objects.filter(username='testuser').first()
        if not test_user:
            print("❌ Test user not found")
            return False
        
        print(f"✓ Using user: {test_user.username}")
        
        # Count before
        before_count = DailyUsage.objects.filter(user=test_user).count()
        print(f"📊 Records before: {before_count}")
        
        # Create form data format
        form_data = {
            'num_appliances': '2',
            'appliance_0_name': 'Test Fan',
            'appliance_0_units': '6.5',
            'appliance_1_name': 'Test Light',
            'appliance_1_units': '3.2'
        }
        
        print(f"📝 Form data: {form_data}")
        
        # Create mock request with form data
        factory = RequestFactory()
        request = factory.post('/add-usage/', data=form_data)
        request.user = test_user
        
        # Call the view function
        response = save_daily_usage(request)
        
        if isinstance(response, JsonResponse):
            response_data = json.loads(response.content.decode())
            print(f"📤 Response: {json.dumps(response_data, indent=2)}")
            
            if response_data.get('success'):
                print("✅ Form data save operation successful!")
                return True
            else:
                print(f"❌ Form data save failed: {response_data.get('message')}")
                return False
        else:
            print(f"❌ Unexpected response type: {type(response)}")
            return False
            
    except Exception as e:
        print(f"❌ Error during form test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Testing Fixed Save Usage Data Functionality")
    print("=" * 70)
    
    # Test 1: JSON format (what frontend sends)
    json_test = test_json_format_save()
    
    # Test 2: Form data format (for compatibility)
    form_test = test_form_data_format()
    
    print("\n" + "=" * 70)
    print("🎯 TEST RESULTS:")
    print(f"   JSON Format Test: {'✅ PASS' if json_test else '❌ FAIL'}")
    print(f"   Form Data Test: {'✅ PASS' if form_test else '❌ FAIL'}")
    
    if json_test and form_test:
        print("\n🎉 ALL TESTS PASSED!")
        print("The 'Save Usage Data' button should now work correctly!")
        print("\n✅ Fixed Issues:")
        print("   • MongoEngine get_or_create() error resolved")
        print("   • JSON data format handling implemented")
        print("   • Form data format compatibility maintained")
        print("   • MongoDB storage working properly")
        print("\n🌐 Test your application at: http://127.0.0.1:8001")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    return json_test and form_test

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
