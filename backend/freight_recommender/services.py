from .models import FreightType, ContainerType, LoadType, CargoCategory, FreightRecommendation

class FreightRecommendationService:
    """ Service for determining optimal freight recommendations based on cargo specifications """
    
    @staticmethod
    def recommend_freight(
        cargo_weight_kg,
        cargo_volume_cubic_m,
        cargo_category_id,
        destination_type="domestic"
    ):
        """
        Recommend optimal freight type, container type, and load type
        based on cargo characteristics
        """

        try: 
            cargo_category = CargoCategory.objects.get(id=cargo_category_id)

            # Determine Load Type
            load_type = FreightRecommendationService._determine_load_type(cargo_weight_kg, cargo_volume_cubic_m)

            # Determine Container Type (if applicable)
            container_type = None
            if load_type.code in ['FCL', 'LCL']:
                container_type = FreightRecommendationService._determine_container_type(cargo_weight_kg, cargo_volume_cubic_m, cargo_category.requires_temperature_control)

            # Determine Freight Type
            freight_type = FreightRecommendationService._determine_freight_type(cargo_category, destination_type, load_type.code)   

            # Some Additional Notes
            notes = FreightRecommendationService._generate_additional_notes(cargo_category, cargo_weight_kg, destination_type)

            return {
                "freight_type": freight_type,
                "container_type": container_type,
                "load_type": load_type,
                "notes": notes
            }
        
        except Exception as e:
            # Log error and return None
            print(f"Error in recommending freight: {str(e)}")
            return None

    @staticmethod 
    def _determine_load_type(weight_kg, volume_cubic_m):
        """Determines if shipment should be FCL, LCL, or LTL"""

        # Based on Philippine logistics standards, we can assume:

        # These thresholds are arbitrary and should be adjusted based on real-world data
        if volume_cubic_m > 55: # ~80% of a 40ft container
            return LoadType.objects.get(code='FCL')
        elif volume_cubic_m > 15: # Significant volumen but not enough for FCL 
            return LoadType.objects.get(code='LCL')
        else: 
            return LoadType.objects.get(code='LTL')
    
    @staticmethod
    def _determine_container_type(weight_kg, volume_cubic_m, requires_temperature_control):
        """ Determine optimal container type based on cargo characteristics"""

        # Check for refrigerated container requirement
        if requires_temperature_control:
            # Get appropriate reefer container
            if volume_cubic_m > 55:
                return ContainerType.objects.get(name='40ft Reefer')
            else:
                return ContainerType.objects.get(name='20ft Reefer')
            
        # For regular cargo, choose the standard container type based on volume
        if weight_kg > 26500: 
            return ContainerType.objects.get(name='20ft Flat Rack') # For heavy cargo
        elif volume_cubic_m > 67: # Exceeds standard 40ft 
            return ContainerType.objects.get(name='40ft High Cube')
        elif volume_cubic_m > 33: # Between 20ft and 40ft
            return ContainerType.objects.get(name='40ft Standard')
        else: 
            return ContainerType.objects.get(name='20ft Standard')
        
    @staticmethod
    def _determine_freight_type(cargo_category, destination_type, load_type_code):
        """ Determine best freight type based on cargo category and destination """

        if cargo_category.hazardous:
            # For hazardous cargo, prefer specialized freight services
            return FreightType.objects.get(name='Specialized Trucking')
        
        if cargo_category.requires_temperature_control:
            # For temperature-sensitive cargo, prefer refrigerated freight services
            return FreightType.objects.get(name='Reefer Freight')
        
        if cargo_category.name == 'Liquid':
            # For liquid cargo, prefer tankers or specialized freight services
            return FreightType.objects.get(name='Liquid Cargo')
        
        if destination_type == 'international':
            if load_type_code in ['FCL', 'LCL']:
                return FreightType.objects.get(name='Sea Freight')
            else: 
                return FreightType.objects.get(name='Air Freight')
        else:
            # For interisland shipping here in the Philippines, prefer RORO or trucking
            if load_type_code == 'FCL':
                return FreightType.objects.get(name='RORO')
            elif cargo_category.name == 'Heavy Machinery':
                return FreightType.objects.get(name='Specialized Trucking')
            else:
                return FreightType.objects.get(name='Trucking')

    @staticmethod
    def _generate_additional_notes(cargo_category, weight_kg, destination_type):
            """ Generate additional notes based on cargo characteristics """
            notes = []
    
             # Weight limit compliance
            if weight_kg > 21700 and weight_kg < 26500:
                notes.append("Requires 40ft container due to weight limit.")
            elif weight_kg > 26500:
                notes.append("WARNING: Weight exceeds standard container limits. May require special handling or multiple containers.")

            # Hazardous materials
            if cargo_category.hazardous:
                notes.append("Temperature-controlled environment required throughout the supply chain.")
                notes.append("YelloX reefer vehicles maintain temperatures from +10°C to -20°C.")

            # Fragile items
            if cargo_category.fragile:
                notes.append("Handle with care. Fragile items may require special packaging.")

            # International shipping notes
            if destination_type == 'international':
                if cargo_category.name == 'Electronics':
                    notes.append("Requires ICC certification for Bureau of Customs clearance.")
                if cargo_category.name == 'Perishable':
                    notes.append("Requires compliance with ASEAN food safety protocols.")

            return "\n".join(notes)
        