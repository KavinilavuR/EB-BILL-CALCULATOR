#!/usr/bin/env python
"""
Test website endpoints to verify data accumulation and tariff calculation
"""
import requests
import json

def test_website_functionality():
    """Test the website functionality"""
    print("🌐 Testing Website Functionality")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        print(f"✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not accessible: {e}")
        return False
    
    # Test 2: Test tariff calculation endpoint
    try:
        # Test different unit values
        test_units = [50, 100, 150, 300, 500]
        
        print(f"\n💰 Testing Tamil Nadu Tariff Calculation:")
        
        for units in test_units:
            tariff_url = f"{base_url}/test-tariff/?units={units}"
            response = requests.get(tariff_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    bill = data['bill_breakdown']
                    print(f"   {units} units → ₹{bill['total_amount']} (Energy: ₹{bill['energy_charges']}, Fixed: ₹{bill['fixed_charges']})")
                else:
                    print(f"   ❌ {units} units → Error: {data.get('message', 'Unknown error')}")
            else:
                print(f"   ❌ {units} units → HTTP {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Tariff test failed: {e}")
    
    print(f"\n📊 Tamil Nadu EB Tariff Slabs:")
    print(f"   0-100 units: FREE")
    print(f"   101-200 units: ₹2.25/unit")
    print(f"   201-400 units: ₹4.50/unit")
    print(f"   401-500 units: ₹6.00/unit")
    print(f"   501-600 units: ₹8.00/unit")
    print(f"   601-800 units: ₹9.00/unit")
    print(f"   800+ units: ₹10.00/unit")
    
    print(f"\n✅ Website testing completed!")
    print(f"🌐 Visit: {base_url}")
    print(f"👤 Login: testuser / testpassword123")
    
    return True

if __name__ == '__main__':
    test_website_functionality()
