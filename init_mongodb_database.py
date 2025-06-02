#!/usr/bin/env python
"""
MongoDB Database Initialization Script for EB Calculator
This script sets up your MongoDB database with initial data and indexes
"""
import sys
import os
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
import django
django.setup()

from bills.models import User, DailyUsage, Appliance, BillCalculation

def create_database_indexes():
    """Create database indexes for better performance"""
    try:
        print("Creating database indexes...")
        
        # User indexes
        User.ensure_indexes()
        print("✓ User indexes created")
        
        # DailyUsage indexes
        DailyUsage.ensure_indexes()
        print("✓ DailyUsage indexes created")
        
        # BillCalculation indexes
        BillCalculation.ensure_indexes()
        print("✓ BillCalculation indexes created")
        
        return True
    except Exception as e:
        print(f"✗ Error creating indexes: {e}")
        return False

def create_admin_user():
    """Create an admin user for the system"""
    try:
        admin_username = 'admin'
        
        # Check if admin user already exists
        existing_admin = User.objects.filter(username=admin_username).first()
        if existing_admin:
            print(f"✓ Admin user '{admin_username}' already exists")
            return existing_admin
        
        # Create admin user
        admin_user = User(
            username=admin_username,
            full_name='System Administrator',
            email='admin@ebcalculator.com',
            phone_number='+91-9999999999',
            address='System Admin Address',
            consumer_number='ADMIN001'
        )
        admin_user.set_password('admin123')  # Change this in production!
        admin_user.save()
        
        print(f"✓ Admin user created: {admin_username} / admin123")
        return admin_user
        
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        return None

def create_sample_user():
    """Create a sample user for testing"""
    try:
        sample_username = 'sampleuser'
        
        # Check if sample user already exists
        existing_user = User.objects.filter(username=sample_username).first()
        if existing_user:
            print(f"✓ Sample user '{sample_username}' already exists")
            return existing_user
        
        # Create sample user
        sample_user = User(
            username=sample_username,
            full_name='Sample User',
            email='sample@example.com',
            phone_number='+91-9876543210',
            address='123 Sample Street, Chennai, Tamil Nadu',
            consumer_number='TN001234567890'
        )
        sample_user.set_password('sample123')
        sample_user.save()
        
        print(f"✓ Sample user created: {sample_username} / sample123")
        return sample_user
        
    except Exception as e:
        print(f"✗ Error creating sample user: {e}")
        return None

def create_sample_usage_data(user, days=30):
    """Create sample usage data for testing"""
    try:
        print(f"Creating {days} days of sample usage data...")
        
        # Common appliances with typical daily usage
        appliance_templates = [
            {'name': 'Fan', 'base_units': 8.0, 'variation': 0.3},
            {'name': 'Light', 'base_units': 5.0, 'variation': 0.2},
            {'name': 'TV', 'base_units': 4.5, 'variation': 0.4},
            {'name': 'Refrigerator', 'base_units': 12.0, 'variation': 0.1},
            {'name': 'AC', 'base_units': 15.0, 'variation': 0.5},
        ]
        
        created_count = 0
        today = datetime.now().date()
        
        for i in range(days):
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
            
            # Add appliances with random variation
            import random
            for template in appliance_templates:
                # Skip some appliances randomly (not all appliances used every day)
                if random.random() < 0.8:  # 80% chance to use each appliance
                    variation = random.uniform(1 - template['variation'], 1 + template['variation'])
                    units = template['base_units'] * variation
                    
                    appliance = Appliance(
                        name=template['name'],
                        units_consumed=round(units, 2)
                    )
                    usage_record.appliances.append(appliance)
            
            usage_record.save()
            created_count += 1
            
            if created_count % 10 == 0:
                print(f"  Created {created_count} records...")
        
        print(f"✓ Created {created_count} daily usage records")
        return created_count
        
    except Exception as e:
        print(f"✗ Error creating sample usage data: {e}")
        return 0

def show_database_summary():
    """Show a summary of the database contents"""
    try:
        print("\n📊 Database Summary:")
        print("=" * 40)
        
        user_count = User.objects.count()
        usage_count = DailyUsage.objects.count()
        bill_count = BillCalculation.objects.count()
        
        print(f"Users: {user_count}")
        print(f"Daily Usage Records: {usage_count}")
        print(f"Bill Calculations: {bill_count}")
        
        if user_count > 0:
            print("\nUsers in database:")
            for user in User.objects.all():
                usage_records = DailyUsage.objects.filter(user=user).count()
                print(f"  - {user.username} ({user.full_name}) - {usage_records} usage records")
        
        if usage_count > 0:
            latest_usage = DailyUsage.objects.order_by('-date').first()
            oldest_usage = DailyUsage.objects.order_by('date').first()
            print(f"\nUsage data range:")
            print(f"  From: {oldest_usage.date.strftime('%Y-%m-%d')}")
            print(f"  To: {latest_usage.date.strftime('%Y-%m-%d')}")
        
    except Exception as e:
        print(f"Error getting database summary: {e}")

def main():
    """Main initialization function"""
    print("🚀 MongoDB Database Initialization for EB Calculator")
    print("=" * 60)
    
    # Step 1: Create indexes
    print("\n1. Setting up database indexes...")
    if not create_database_indexes():
        print("❌ Failed to create indexes")
        return False
    
    # Step 2: Create admin user
    print("\n2. Creating admin user...")
    admin_user = create_admin_user()
    if not admin_user:
        print("❌ Failed to create admin user")
        return False
    
    # Step 3: Create sample user
    print("\n3. Creating sample user...")
    sample_user = create_sample_user()
    if not sample_user:
        print("❌ Failed to create sample user")
        return False
    
    # Step 4: Create sample data
    print("\n4. Creating sample usage data...")
    created_records = create_sample_usage_data(sample_user, days=60)  # 2 months of data
    
    # Step 5: Show summary
    show_database_summary()
    
    print("\n✅ Database initialization complete!")
    print("\nLogin credentials:")
    print("  Admin: admin / admin123")
    print("  Sample User: sampleuser / sample123")
    print("\nYour MongoDB database is ready for the EB Calculator!")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInitialization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        sys.exit(1)
