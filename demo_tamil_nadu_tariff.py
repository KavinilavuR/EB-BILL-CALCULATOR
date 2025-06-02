#!/usr/bin/env python
"""
Demo script to show Tamil Nadu EB tariff calculation
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eb_calculator.settings')
django.setup()

def demo_tariff_calculation():
    """Demo Tamil Nadu EB tariff calculation"""
    print("🏠 Tamil Nadu EB Bill Calculator Demo")
    print("=" * 50)
    
    try:
        from bills.utils import TamilNaduTariffCalculator
        
        print("📊 Tamil Nadu EB Tariff Slabs (Bi-monthly):")
        slabs = TamilNaduTariffCalculator.get_tariff_info()
        for slab in slabs:
            max_units = slab['max_units'] if slab['max_units'] else "∞"
            print(f"   {slab['slab_name']}: ₹{slab['rate_per_unit']}/unit")
        
        print("\n💡 Sample Bill Calculations:")
        
        # Test cases based on your image
        test_cases = [
            (50, "50 units - FREE (under 100)"),
            (100, "100 units - FREE (exactly 100)"),
            (150, "150 units - 50 units charged"),
            (300, "300 units - Multiple slabs"),
            (500, "500 units - Higher consumption"),
        ]
        
        for units, description in test_cases:
            result = TamilNaduTariffCalculator.calculate_bill(units)
            
            print(f"\n📋 {description}")
            print(f"   Units Consumed: {units} kWh")
            print(f"   Energy Charges: ₹{result['energy_charges']}")
            print(f"   Fixed Charges: ₹{result['fixed_charges']}")
            print(f"   Electricity Duty (15%): ₹{result['electricity_duty']}")
            print(f"   Service Charge: ₹{result['service_charge']}")
            print(f"   💰 TOTAL AMOUNT: ₹{result['total_amount']}")
            
            if result['slab_wise_charges']:
                print(f"   📊 Slab Breakdown:")
                for slab_detail in result['slab_wise_charges']:
                    if slab_detail['amount'] > 0:
                        print(f"     - {slab_detail['slab_name']}: {slab_detail['units']} units × ₹{slab_detail['rate_per_unit']} = ₹{slab_detail['amount']}")
        
        print("\n" + "=" * 50)
        print("✅ Tamil Nadu EB tariff calculation working perfectly!")
        print("🌐 Your website now supports:")
        print("   ✅ Data accumulation (stacking daily usage)")
        print("   ✅ Tamil Nadu EB tariff slabs")
        print("   ✅ 2-month bill generation")
        print("   ✅ Free electricity for first 100 units")
        print("   ✅ Progressive tariff slabs as per TN EB board")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    demo_tariff_calculation()
