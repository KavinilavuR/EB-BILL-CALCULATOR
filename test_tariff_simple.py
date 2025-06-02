#!/usr/bin/env python
"""
Simple test to verify Tamil Nadu tariff calculation
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
django.setup()

def test_tariff():
    """Test Tamil Nadu tariff calculation"""
    from bills.utils import TamilNaduTariffCalculator
    
    print("🧮 Tamil Nadu EB Tariff Test")
    print("=" * 40)
    
    # Test cases
    test_cases = [85, 100, 150, 200]
    
    for units in test_cases:
        result = TamilNaduTariffCalculator.calculate_bill(units)
        print(f"\n📊 {units} units:")
        print(f"   Energy Charges: ₹{result['energy_charges']}")
        print(f"   Fixed Charges: ₹{result['fixed_charges']}")
        print(f"   Electricity Duty: ₹{result['electricity_duty']}")
        print(f"   Service Charge: ₹{result['service_charge']}")
        print(f"   💰 TOTAL: ₹{result['total_amount']}")
        
        if units <= 100:
            expected_energy = 0.0
            expected_total = 25.0  # Only service charge
            if result['energy_charges'] == expected_energy and result['total_amount'] == expected_total:
                print(f"   ✅ CORRECT - FREE electricity under 100 units")
            else:
                print(f"   ❌ ERROR - Should be FREE (₹25 service charge only)")
        else:
            print(f"   ℹ️  Above 100 units - charges apply")

if __name__ == '__main__':
    test_tariff()
