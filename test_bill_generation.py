#!/usr/bin/env python3
"""
Test script to verify bill generation functionality
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
django.setup()

from bills.models import User, DailyUsage, BillCalculation, Appliance
from bills.utils import TamilNaduTariffCalculator, generate_invoice_number

def test_bill_generation():
    """Test the complete bill generation process"""
    print("🔧 Testing Bill Generation Process...")
    
    # 1. Test invoice number generation
    print("\n1. Testing invoice number generation...")
    invoice_num = generate_invoice_number()
    print(f"   Generated invoice number: {invoice_num}")
    print(f"   Length: {len(invoice_num)} characters")
    
    # 2. Test tariff calculation
    print("\n2. Testing Tamil Nadu tariff calculation...")
    test_units = [50, 150, 250, 400]
    for units in test_units:
        bill_breakdown = TamilNaduTariffCalculator.calculate_bill(units)
        print(f"   {units} units -> ₹{bill_breakdown['total_amount']:.2f}")
    
    # 3. Check if test user exists
    print("\n3. Checking for test user...")
    try:
        user = User.objects.get(username='testuser')
        print(f"   Found user: {user.username}")
    except User.DoesNotExist:
        print("   Test user not found. Creating one...")
        user = User(
            username='testuser',
            email='test@example.com',
            full_name='Test User'
        )
        user.set_password('testpass123')
        user.save()
        print(f"   Created user: {user.username}")
    
    # 4. Check existing usage data
    print("\n4. Checking existing usage data...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    
    usage_records = DailyUsage.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    total_units = sum(record.total_units for record in usage_records)
    print(f"   Found {len(usage_records)} usage records")
    print(f"   Total units in last 60 days: {total_units:.2f} kWh")
    
    if len(usage_records) == 0:
        print("   No usage data found. Adding sample data...")
        # Add some sample usage data
        sample_dates = [
            datetime.now() - timedelta(days=i) 
            for i in range(1, 31)  # Last 30 days
        ]
        
        for date in sample_dates:
            # Create sample appliances
            appliances = [
                Appliance(name="LED Bulb", units_consumed=0.5),
                Appliance(name="Fan", units_consumed=2.0),
                Appliance(name="TV", units_consumed=1.5),
            ]
            
            daily_usage = DailyUsage(
                user=user,
                date=date,
                appliances=appliances,
                notes=f"Sample data for {date.strftime('%Y-%m-%d')}"
            )
            daily_usage.save()
        
        print(f"   Added sample usage data for 30 days")
        
        # Recalculate total
        usage_records = DailyUsage.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        )
        total_units = sum(record.total_units for record in usage_records)
        print(f"   New total units: {total_units:.2f} kWh")
    
    # 5. Test bill generation
    print("\n5. Testing bill generation...")
    if total_units > 0:
        bill_breakdown = TamilNaduTariffCalculator.calculate_bill(total_units)
        print(f"   Bill breakdown for {total_units:.2f} units:")
        print(f"   - Energy charges: ₹{bill_breakdown['energy_charges']:.2f}")
        print(f"   - Fixed charges: ₹{bill_breakdown['fixed_charges']:.2f}")
        print(f"   - Electricity duty: ₹{bill_breakdown['electricity_duty']:.2f}")
        print(f"   - Service charge: ₹{bill_breakdown['service_charge']:.2f}")
        print(f"   - Total amount: ₹{bill_breakdown['total_amount']:.2f}")
        
        # Create a test bill
        from bills.utils import calculate_billing_period
        billing_start, billing_end = calculate_billing_period()
        
        bill = BillCalculation(
            user=user,
            billing_period_start=billing_start,
            billing_period_end=billing_end,
            previous_reading=0,
            current_reading=total_units,
            units_consumed=total_units,
            energy_charges=bill_breakdown['energy_charges'],
            fixed_charges=bill_breakdown['fixed_charges'],
            additional_charges=bill_breakdown['electricity_duty'] + bill_breakdown['service_charge'],
            total_amount=bill_breakdown['total_amount']
        )
        bill.save()
        
        print(f"   Created bill with invoice number: {bill.invoice_number}")
        print(f"   Bill ID: {bill.id}")
        print(f"   Due date: {bill.due_date.strftime('%Y-%m-%d')}")
        
        return bill.id
    else:
        print("   No usage data available for bill generation")
        return None

if __name__ == "__main__":
    try:
        bill_id = test_bill_generation()
        if bill_id:
            print(f"\n✅ Bill generation test completed successfully!")
            print(f"   You can view the bill at: http://127.0.0.1:8000/bill-invoice/?bill_id={bill_id}")
        else:
            print(f"\n❌ Bill generation test failed - no usage data")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
