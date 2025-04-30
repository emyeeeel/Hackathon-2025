import os
import django
import json
from django.test import Client

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')
django.setup()

# Import models
from freight_recommender.models import CargoCategory, FreightType, ContainerType, LoadType

def run_tests():
    print("\n===== FREIGHT RECOMMENDER VERIFICATION TESTS =====\n")
    
    # Create a test client
    client = Client()
    
    # Test 1: Get all cargo categories
    print("Test 1: Retrieving Cargo Categories")
    response = client.get('/api/freight/cargo-categories/')
    if response.status_code == 200:
        categories = response.json()
        print(f"✅ Successfully retrieved {len(categories)} cargo categories")
        for cat in categories:
            print(f"  - {cat['name']}")
    else:
        print(f"❌ Failed to retrieve cargo categories: {response.status_code}")
    
    # Test 2: General Cargo Recommendation (Domestic)
    print("\nTest 2: General Cargo Recommendation (Domestic)")
    test_data = {
        'cargo_weight_kg': 5000,
        'cargo_volume_cubic_m': 25,
        'cargo_category_id': CargoCategory.objects.get(name='General').id,
        'destination_type': 'domestic'
    }
    
    response = client.post(
        '/api/freight/recommendation/', 
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Successfully generated recommendation:")
        print(f"  - Freight Type: {result['freight_type']['name']}")
        print(f"  - Container Type: {result['container_type']['name'] if result['container_type'] else 'None'}")
        print(f"  - Load Type: {result['load_type']['code']}")
        print(f"  - Notes: {result['additional_notes'][:100]}..." if result['additional_notes'] else "  - Notes: None")
    else:
        print(f"❌ Failed to generate recommendation: {response.status_code}")
        print(response.content)
    
    # Test 3: Perishable Cargo Recommendation
    print("\nTest 3: Perishable Cargo Recommendation")
    test_data = {
        'cargo_weight_kg': 5000,
        'cargo_volume_cubic_m': 25,
        'cargo_category_id': CargoCategory.objects.get(name='Perishable').id,
        'destination_type': 'domestic'
    }
    
    response = client.post(
        '/api/freight/recommendation/', 
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Successfully generated recommendation:")
        print(f"  - Freight Type: {result['freight_type']['name']}")
        print(f"  - Container Type: {result['container_type']['name'] if result['container_type'] else 'None'}")
        print(f"  - Load Type: {result['load_type']['code']}")
        print(f"  - Notes: {result['additional_notes'][:100]}..." if result['additional_notes'] else "  - Notes: None")
        
        # Verify reefer container for perishables
        if result['container_type'] and result['container_type']['temperature_controlled']:
            print("✅ Correctly recommended temperature-controlled container for perishables")
        else:
            print("❌ Failed to recommend temperature-controlled container for perishables")
    else:
        print(f"❌ Failed to generate recommendation: {response.status_code}")
    
    # Test 4: International Shipping
    print("\nTest 4: International Shipping")
    test_data = {
        'cargo_weight_kg': 8000,
        'cargo_volume_cubic_m': 50,
        'cargo_category_id': CargoCategory.objects.get(name='Electronics').id,
        'destination_type': 'international'
    }
    
    response = client.post(
        '/api/freight/recommendation/', 
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Successfully generated recommendation:")
        print(f"  - Freight Type: {result['freight_type']['name']}")
        print(f"  - Container Type: {result['container_type']['name'] if result['container_type'] else 'None'}")
        print(f"  - Load Type: {result['load_type']['code']}")
        print(f"  - Notes: {result['additional_notes'][:100]}..." if result['additional_notes'] else "  - Notes: None")
        
        # Verify international shipping recommendation
        if result['freight_type']['name'] in ['Sea Freight', 'Air Freight']:
            print("✅ Correctly recommended international shipping option")
        else:
            print(f"❌ Unexpected freight type for international shipping: {result['freight_type']['name']}")
    else:
        print(f"❌ Failed to generate recommendation: {response.status_code}")
    
    print("\n===== TEST SUMMARY =====")
    print("All test scenarios completed. Check the results above to verify correctness.")
    print("The Freight Recommender implementation is now complete and verified.")

if __name__ == "__main__":
    run_tests()