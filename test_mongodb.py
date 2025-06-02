#!/usr/bin/env python
"""
Simple test script to verify MongoDB integration
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
django.setup()

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from mongoengine import connect
        connect('eb_calculator_db', host='localhost', port=27017)
        print("✓ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

def test_models():
    """Test model creation"""
    try:
        from bills.models import User, DailyUsage, Appliance
        from datetime import datetime
        
        # Test user creation
        test_user = User(
            username='test_mongo_user',
            full_name='Test MongoDB User',
            email='test@example.com'
        )
        test_user.set_password('testpass123')
        
        # Check if user already exists
        existing_user = User.objects.filter(username='test_mongo_user').first()
        if existing_user:
            print("✓ Test user already exists")
            test_user = existing_user
        else:
            test_user.save()
            print("✓ Test user created successfully")
        
        # Test daily usage creation
        usage_record = DailyUsage(
            user=test_user,
            date=datetime.now(),
            appliances=[]
        )
        
        # Add test appliances
        appliance1 = Appliance(name='Test Fan', units_consumed=5.5)
        appliance2 = Appliance(name='Test Light', units_consumed=3.2)
        
        usage_record.appliances.append(appliance1)
        usage_record.appliances.append(appliance2)
        
        usage_record.save()
        print(f"✓ Daily usage record created: {usage_record.total_units} kWh")
        
        # Test tariff calculation
        from bills.utils import TamilNaduTariffCalculator
        bill_breakdown = TamilNaduTariffCalculator.calculate_bill(usage_record.total_units)
        print(f"✓ Tariff calculation successful: ₹{bill_breakdown['total_amount']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=== MongoDB Integration Test ===")
    print()
    
    # Test MongoDB connection
    if not test_mongodb_connection():
        print("\nPlease ensure MongoDB is running on localhost:27017")
        return
    
    # Test models
    print("\nTesting models...")
    if test_models():
        print("\n✓ All tests passed! MongoDB integration is working correctly.")
        print("\nYou can now:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://localhost:8000")
        print("3. Login with sample credentials or create a new account")
    else:
        print("\n✗ Some tests failed. Please check the error messages above.")

if __name__ == '__main__':
    main()
