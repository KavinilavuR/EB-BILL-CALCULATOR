#!/usr/bin/env python
"""
Create a user for the website to test with
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

from bills.models import User

def create_website_user():
    """Create a user for testing the website"""
    print("👤 Creating Website User...")
    
    try:
        # Check if user already exists
        username = 'testuser'
        existing_user = User.objects.filter(username=username).first()
        
        if existing_user:
            print(f"✅ User '{username}' already exists")
            return existing_user
        
        # Create new user
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
        
        print(f"✅ Created user: {username}")
        print(f"   Password: testpassword123")
        print(f"   Full name: {user.full_name}")
        print(f"   Email: {user.email}")
        print(f"   Consumer number: {user.consumer_number}")
        
        return user
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return None

def main():
    print("🚀 Creating Website User for Testing")
    print("=" * 50)
    
    user = create_website_user()
    
    if user:
        print("\n✅ User creation successful!")
        print("\n🌐 Login credentials for your website:")
        print("   Username: testuser")
        print("   Password: testpassword123")
        print("\n📝 You can now:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://localhost:8000")
        print("3. Login with the above credentials")
        print("4. Test the 'Save Usage Data' button")
        print("5. Data will be saved to: eb_calculator_website_db")
    else:
        print("\n❌ User creation failed!")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
