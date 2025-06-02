#!/usr/bin/env python
"""
Direct MongoDB Test for EB Calculator
This tests the MongoDB integration by directly creating and saving data
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

from bills.models import User, DailyUsage, Appliance

def test_direct_mongodb_save():
    """Test saving data directly to MongoDB"""
    print("🧪 Direct MongoDB Save Test")
    print("=" * 40)
    
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
        
        # Create new usage record
        usage_record = DailyUsage(
            user=test_user,
            date=datetime.now(),
            appliances=[]
        )
        
        # Add test appliances
        appliances_data = [
            {'name': 'Test Fan', 'units': 8.5},
            {'name': 'Test Light', 'units': 5.2},
            {'name': 'Test TV', 'units': 4.8}
        ]
        
        for app_data in appliances_data:
            appliance = Appliance(
                name=app_data['name'],
                units_consumed=app_data['units']
            )
            usage_record.appliances.append(appliance)
        
        # Save to MongoDB
        usage_record.save()
        print(f"✅ Saved record with ID: {usage_record.id}")
        print(f"📊 Total units: {usage_record.total_units} kWh")
        
        # Count after
        after_count = DailyUsage.objects.filter(user=test_user).count()
        print(f"📊 Records after: {after_count}")
        
        if after_count > before_count:
            print("✅ Data successfully saved to MongoDB!")
            return True
        else:
            print("❌ Data was not saved")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_bill_calculation_with_mongodb_data():
    """Test bill calculation using MongoDB data"""
    print("\n💰 Bill Calculation Test with MongoDB Data")
    print("=" * 50)
    
    try:
        # Get test user
        test_user = User.objects.filter(username='testuser').first()
        if not test_user:
            print("❌ Test user not found")
            return False
        
        # Get usage data for last 60 days (2 months)
        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=60)
        
        usage_records = DailyUsage.objects.filter(
            user=test_user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        print(f"📅 Usage records found (last 60 days): {usage_records.count()}")
        
        if usage_records.count() == 0:
            print("❌ No usage data found for bill calculation")
            return False
        
        # Calculate total units
        total_units = sum(record.total_units for record in usage_records)
        print(f"⚡ Total units consumed: {total_units:.2f} kWh")
        
        # Test Tamil Nadu tariff calculation
        from bills.utils import TamilNaduTariffCalculator
        bill_breakdown = TamilNaduTariffCalculator.calculate_bill(total_units)
        
        print(f"💰 Bill calculation results:")
        print(f"   Energy charges: ₹{bill_breakdown['energy_charges']:.2f}")
        print(f"   Fixed charges: ₹{bill_breakdown['fixed_charges']:.2f}")
        print(f"   Electricity duty: ₹{bill_breakdown['electricity_duty']:.2f}")
        print(f"   Service charge: ₹{bill_breakdown['service_charge']:.2f}")
        print(f"   Total amount: ₹{bill_breakdown['total_amount']:.2f}")
        
        print("✅ Bill calculation successful with MongoDB data!")
        return True
        
    except Exception as e:
        print(f"❌ Error in bill calculation: {e}")
        return False

def test_user_authentication():
    """Test user authentication with MongoDB"""
    print("\n🔐 User Authentication Test")
    print("=" * 30)
    
    try:
        # Test user login
        test_user = User.objects.filter(username='testuser').first()
        if not test_user:
            print("❌ Test user not found")
            return False
        
        # Test password verification
        if test_user.check_password('testpassword123'):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
            return False
        
        # Test user data
        print(f"👤 User details:")
        print(f"   Username: {test_user.username}")
        print(f"   Full name: {test_user.full_name}")
        print(f"   Email: {test_user.email}")
        print(f"   Consumer number: {test_user.consumer_number}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in authentication test: {e}")
        return False

def show_mongodb_summary():
    """Show complete MongoDB database summary"""
    print("\n📊 Complete MongoDB Database Summary")
    print("=" * 50)
    
    try:
        # Users summary
        users = User.objects.all()
        print(f"👥 Total users: {users.count()}")
        
        for user in users:
            usage_count = DailyUsage.objects.filter(user=user).count()
            if usage_count > 0:
                latest_usage = DailyUsage.objects.filter(user=user).order_by('-date').first()
                total_consumption = sum(record.total_units for record in DailyUsage.objects.filter(user=user))
                print(f"   {user.username}: {usage_count} records, {total_consumption:.2f} total kWh")
                print(f"     Latest: {latest_usage.date.strftime('%Y-%m-%d')} ({latest_usage.total_units:.2f} kWh)")
        
        # Overall statistics
        total_usage_records = DailyUsage.objects.count()
        total_consumption = sum(record.total_units for record in DailyUsage.objects.all())
        
        print(f"\n📈 Overall Statistics:")
        print(f"   Total usage records: {total_usage_records}")
        print(f"   Total consumption tracked: {total_consumption:.2f} kWh")
        
        if total_usage_records > 0:
            avg_daily = total_consumption / total_usage_records
            print(f"   Average daily consumption: {avg_daily:.2f} kWh")
        
        return True
        
    except Exception as e:
        print(f"❌ Error getting summary: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Complete MongoDB Integration Test")
    print("=" * 60)
    
    # Test 1: Direct MongoDB save
    save_test = test_direct_mongodb_save()
    
    # Test 2: Bill calculation with MongoDB data
    bill_test = test_bill_calculation_with_mongodb_data()
    
    # Test 3: User authentication
    auth_test = test_user_authentication()
    
    # Test 4: Database summary
    summary_test = show_mongodb_summary()
    
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS:")
    print(f"   Direct MongoDB Save: {'✅ PASS' if save_test else '❌ FAIL'}")
    print(f"   Bill Calculation: {'✅ PASS' if bill_test else '❌ FAIL'}")
    print(f"   User Authentication: {'✅ PASS' if auth_test else '❌ FAIL'}")
    print(f"   Database Summary: {'✅ PASS' if summary_test else '❌ FAIL'}")
    
    all_passed = save_test and bill_test and auth_test and summary_test
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your MongoDB integration is working perfectly!")
        print("\n✅ Ready for production use:")
        print("   • User authentication with MongoDB")
        print("   • Daily usage data storage")
        print("   • 2-month bill calculation")
        print("   • Tamil Nadu EB tariff integration")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
