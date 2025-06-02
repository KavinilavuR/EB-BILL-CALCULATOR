#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
django.setup()

print("🚀 Quick Test")

try:
    from bills.models import User
    from bills.utils import TamilNaduTariffCalculator
    
    # Test user
    users = User.objects.all()
    print(f"👤 Users in database: {users.count()}")
    for user in users:
        print(f"   - {user.username}")
    
    # Test tariff
    result = TamilNaduTariffCalculator.calculate_bill(150)
    print(f"💰 150 units bill: ₹{result['total_amount']}")
    
    print("✅ Quick test completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
