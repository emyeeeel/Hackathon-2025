# Create a new file:
# filepath: c:\Users\AJ\Documents\SCHOOL NEEDS\2ND SEM 2024 - 2025\HACKATHON 2025\Hackathon-2025\backend\freight_recommender\management\commands\list_freight_data.py

from django.core.management.base import BaseCommand
from freight_recommender.models import FreightType, ContainerType, LoadType, CargoCategory

class Command(BaseCommand):
    help = 'Lists all freight recommendation data categories and their details'

    def handle(self, *args, **kwargs):
        self._list_cargo_categories()
        self._list_freight_types()
        self._list_container_types()
        self._list_load_types()

    def _list_cargo_categories(self):
        self.stdout.write(self.style.NOTICE("\n=== CARGO CATEGORIES ==="))
        categories = CargoCategory.objects.all()
        
        for cat in categories:
            special = []
            if cat.requires_temperature_control:
                special.append("Temp-controlled")
            if cat.hazardous:
                special.append("Hazardous")
            if cat.fragile:
                special.append("Fragile")
                
            special_str = ", ".join(special) if special else "None"
            
            self.stdout.write(f"{cat.name} - Special Requirements: {special_str}")
            self.stdout.write(f"  Details: {cat.special_requirements}")
            
        self.stdout.write(f"\nTotal: {categories.count()} cargo categories")

    def _list_freight_types(self):
        self.stdout.write(self.style.NOTICE("\n=== FREIGHT TYPES ==="))
        freight_types = FreightType.objects.all()
        
        for ft in freight_types:
            self.stdout.write(f"{ft.name}")
            self.stdout.write(f"  Description: {ft.description}")
            
        self.stdout.write(f"\nTotal: {freight_types.count()} freight types")

    def _list_container_types(self):
        self.stdout.write(self.style.NOTICE("\n=== CONTAINER TYPES ==="))
        container_types = ContainerType.objects.all()
        
        for ct in container_types:
            temp = "Temperature-controlled" if ct.temperature_controlled else "Regular"
            self.stdout.write(f"{ct.name} ({temp})")
            self.stdout.write(f"  Dimensions: {ct.length_cm}cm x {ct.width_cm}cm x {ct.height_cm}cm")
            self.stdout.write(f"  Capacity: {ct.volume_cubic_m}m³, Max weight: {ct.max_weight_kg}kg")
            
        self.stdout.write(f"\nTotal: {container_types.count()} container types")

    def _list_load_types(self):
        self.stdout.write(self.style.NOTICE("\n=== LOAD TYPES ==="))
        load_types = LoadType.objects.all()
        
        for lt in load_types:
            self.stdout.write(f"{lt.code}: {lt.name}")
            self.stdout.write(f"  Description: {lt.description}")
            
        self.stdout.write(f"\nTotal: {load_types.count()} load types")