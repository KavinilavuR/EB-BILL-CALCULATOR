#!/usr/bin/env python
"""
Complete MongoDB Setup Script for EB Calculator
This script handles MongoDB connection, database setup, and initial data creation
"""
import os
import sys
import django
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_mongodb_connection():
    """Check if MongoDB is running and accessible"""
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
        client.server_info()  # Force connection
        print("✓ MongoDB is running on localhost:27017")
        return True
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("\nPlease ensure MongoDB is running:")
        print("  Windows: net start MongoDB")
        print("  macOS: brew services start mongodb-community")
        print("  Linux: sudo systemctl start mongod")
        return False

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
django.setup()

from bills.models import User, DailyUsage, Appliance


def create_sample_user():
    """Create a sample user for testing"""
    username = 'testuser'
    
    try:
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists.")
        return user
    except User.DoesNotExist:
        user = User(
            username=username,
            full_name='Test User',
            email='testuser@example.com',
            phone_number='+91-9876543210',
            address='123 Test Street, Chennai, Tamil Nadu',
            consumer_number='TN001234567890'
        )
        user.set_password('testpassword123')
        user.save()
        print(f"Created sample user: {username}")
        print(f"Password: testpassword123")
        return user


def create_sample_usage_data(user):
    """Create some sample usage data"""
    from datetime import date, timedelta
    
    # Sample appliances with typical usage
    sample_appliances = [
        {'name': 'Fan', 'units': 8.5},
        {'name': 'Light', 'units': 5.2},
        {'name': 'TV', 'units': 4.8},
        {'name': 'Refrigerator', 'units': 12.0},
    ]
    
    # Create usage data for the last 30 days
    today = date.today()
    created_count = 0
    
    for i in range(30):
        usage_date = today - timedelta(days=i)
        
        # Check if record already exists
        existing = DailyUsage.objects.filter(
            user=user,
            date__gte=datetime.combine(usage_date, datetime.min.time()),
            date__lt=datetime.combine(usage_date, datetime.max.time())
        ).first()
        
        if existing:
            continue
            
        # Create daily usage record
        usage_record = DailyUsage(
            user=user,
            date=datetime.combine(usage_date, datetime.min.time()),
            appliances=[]
        )
        
        # Add appliances with some variation
        import random
        for app_data in sample_appliances:
            # Add some random variation (±20%)
            variation = random.uniform(0.8, 1.2)
            units = app_data['units'] * variation
            
            appliance = Appliance(
                name=app_data['name'],
                units_consumed=round(units, 2)
            )
            usage_record.appliances.append(appliance)
        
        usage_record.save()
        created_count += 1
        print(f"Created usage data for {usage_date}: {usage_record.total_units:.2f} kWh")
    
    print(f"Created {created_count} daily usage records")


def main():
    """Main setup function"""
    print("🚀 EB Calculator MongoDB Setup")
    print("=" * 50)

    # Step 1: Check MongoDB connection
    print("\n1. Checking MongoDB connection...")
    if not check_mongodb_connection():
        return False

    # Step 2: Test Django-MongoDB integration
    print("\n2. Testing Django-MongoDB integration...")
    try:
        from mongoengine import connect
        connect('eb_calculator_db', host='localhost', port=27017)
        print("✓ Django-MongoDB integration successful")
    except Exception as e:
        print(f"✗ Django-MongoDB integration failed: {e}")
        return False

    # Step 3: Create sample user
    print("\n3. Creating sample user...")
    user = create_sample_user()
    if not user:
        return False

    # Step 4: Create sample usage data
    print("\n4. Creating sample usage data...")
    create_sample_usage_data(user)

    # Step 5: Show database info
    print("\n5. Database Summary:")
    try:
        user_count = User.objects.count()
        usage_count = DailyUsage.objects.count()
        print(f"   Users: {user_count}")
        print(f"   Usage Records: {usage_count}")
    except Exception as e:
        print(f"   Error getting counts: {e}")

    print("\n✅ Setup Complete!")
    print("=" * 50)
    print("Login Credentials:")
    print("  Username: testuser")
    print("  Password: testpassword123")
    print()
    print("Next Steps:")
    print("1. python manage.py runserver")
    print("2. Visit: http://localhost:8000")
    print("3. Login and start tracking your electricity usage!")
    print()
    print("Optional - Import existing data:")
    print("python manage.py import_energy_data --username testuser --file 'energyFILE (1).txt'")

    return True


if __name__ == '__main__':
    main()
