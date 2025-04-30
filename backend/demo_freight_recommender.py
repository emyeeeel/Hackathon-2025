import os
import django
import json
from django.test import Client
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')
django.setup()

# Import models
from freight_recommender.models import CargoCategory, FreightType, ContainerType, LoadType
from freight_recommender.services import FreightRecommendationService

def show_demo():
    """Interactive demo for the freight recommender"""
    
    print("\n\n===============================================")
    print("    GOTHONG SOUTHERN FREIGHT RECOMMENDER DEMO    ")
    print("===============================================\n")
    
    print("This system recommends the optimal freight options based on cargo characteristics.")
    print("Let's explore a few scenarios to demonstrate how it works...\n")
    
    time.sleep(2)
    
    # Show available cargo categories
    categories = CargoCategory.objects.all()
    print("Available cargo categories:")
    for i, category in enumerate(categories, 1):
        special_attrs = []
        if category.requires_temperature_control:
            special_attrs.append("temperature-controlled")
        if category.hazardous:
            special_attrs.append("hazardous")
        if category.fragile:
            special_attrs.append("fragile")
        
        attr_str = f" ({', '.join(special_attrs)})" if special_attrs else ""
        print(f"  {i}. {category.name}{attr_str}")
    
    print("\nNow, let's see what recommendations our system provides for different scenarios.")
    time.sleep(2)
    
    # Scenario 1: General Cargo (Small Domestic)
    print("\n\n===== SCENARIO 1: GENERAL CARGO (SMALL DOMESTIC) =====")
    print("Cargo details:")
    print("  - Type: General cargo")
    print("  - Weight: 1,000 kg")
    print("  - Volume: 10 cubic meters")
    print("  - Destination: Domestic")
    
    input("\nPress Enter to generate recommendation...")
    
    general = CargoCategory.objects.get(name='General')
    recommendation = FreightRecommendationService.recommend_freight(
        cargo_weight_kg=1000,
        cargo_volume_cubic_m=10,
        cargo_category_id=general.id,
        destination_type='domestic'
    )
    
    print("\nRECOMMENDATION:")
    print(f"  🚚 Freight Type: {recommendation['freight_type'].name}")
    print(f"  📦 Container Type: {recommendation['container_type'].name if recommendation['container_type'] else 'N/A'}")
    print(f"  🔄 Load Type: {recommendation['load_type'].code} ({recommendation['load_type'].name})")
    print(f"  📝 Handling Notes: {recommendation['notes']}")
    
    print("\nEXPLANATION:")
    print("  - LTL (Less than Truck Load) was recommended because the volume is small")
    print("  - Trucking is recommended for domestic small shipments")
    print("  - No container needed as this is trucking service")
    
    # Scenario 2: Perishable Goods
    time.sleep(2)
    print("\n\n===== SCENARIO 2: PERISHABLE GOODS =====")
    print("Cargo details:")
    print("  - Type: Perishable goods (requires temperature control)")
    print("  - Weight: 5,000 kg")
    print("  - Volume: 20 cubic meters")
    print("  - Destination: Domestic")
    
    input("\nPress Enter to generate recommendation...")
    
    perishable = CargoCategory.objects.get(name='Perishable')
    recommendation = FreightRecommendationService.recommend_freight(
        cargo_weight_kg=5000,
        cargo_volume_cubic_m=20,
        cargo_category_id=perishable.id,
        destination_type='domestic'
    )
    
    print("\nRECOMMENDATION:")
    print(f"  🚚 Freight Type: {recommendation['freight_type'].name}")
    print(f"  📦 Container Type: {recommendation['container_type'].name if recommendation['container_type'] else 'N/A'}")
    print(f"  🔄 Load Type: {recommendation['load_type'].code} ({recommendation['load_type'].name})")
    print(f"  📝 Handling Notes: {recommendation['notes']}")
    
    print("\nEXPLANATION:")
    print("  - Reefer Freight was recommended because the cargo requires temperature control")
    print("  - A temperature-controlled container (Reefer) was selected")
    print("  - Temperature control is maintained throughout the supply chain")
    
    # Scenario 3: International Shipping
    time.sleep(2)
    print("\n\n===== SCENARIO 3: INTERNATIONAL SHIPPING =====")
    print("Cargo details:")
    print("  - Type: Electronics (fragile)")
    print("  - Weight: 10,000 kg")
    print("  - Volume: 50 cubic meters")
    print("  - Destination: International")
    
    input("\nPress Enter to generate recommendation...")
    
    electronics = CargoCategory.objects.get(name='Electronics')
    recommendation = FreightRecommendationService.recommend_freight(
        cargo_weight_kg=10000,
        cargo_volume_cubic_m=50,
        cargo_category_id=electronics.id,
        destination_type='international'
    )
    
    print("\nRECOMMENDATION:")
    print(f"  🚚 Freight Type: {recommendation['freight_type'].name}")
    print(f"  📦 Container Type: {recommendation['container_type'].name if recommendation['container_type'] else 'N/A'}")
    print(f"  🔄 Load Type: {recommendation['load_type'].code} ({recommendation['load_type'].name})")
    print(f"  📝 Handling Notes: {recommendation['notes']}")
    
    print("\nEXPLANATION:")
    print("  - Sea Freight was recommended for international shipping of large volume")
    print("  - FCL (Full Container Load) was selected due to the large volume")
    print("  - Special handling notes for fragile electronics are provided")
    
    print("\n\n===============================================")
    print("               DEMO COMPLETED                   ")
    print("===============================================")
    print("\nThis demonstration shows how the freight recommender analyzes:")
    print("  1. Cargo characteristics (weight, volume, special requirements)")
    print("  2. Destination type (domestic or international)")
    print("  3. Shipping regulations and requirements")
    print("\nTo make intelligent recommendations for optimal freight options.")
    print("\nThe system is ready for integration with other components!")

if __name__ == "__main__":
    show_demo()