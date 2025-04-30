from django.core.management.base import BaseCommand
from freight_recommender.models import FreightType, ContainerType, LoadType, CargoCategory

class Command(BaseCommand):
    help = 'Seeds freight recommendation datas based on Gothong Southern offerings'

    def handle(self, *args, **kwargs):

        self._create_load_types()

        self._create_container_types()

        self._create_freight_types()

        self._create_cargo_categories()

        self.stdout.write(self.style.SUCCESS('Successfully seeded freight recommendation data.'))

    def _create_load_types(self):
        load_types = [
            {
                'code': 'FCL',
                'name': 'Full Container Load',
                'description': 'The entire container dedicated to one shipment. Ideal for large volume cargo.'
            }, 
            {
                'code': 'LCL',
                'name': 'Less than Container Load',
                'description': 'Shipment shares container space with other cargo. Cost - effective for smaller shipments'
            }, 
            {
                'code': 'LTL',
                'name': 'Less than Truck Load',
                'description': 'Shipment shares truck space with other cargo. Suitable for small domestic deliveries'
            }
        ]

        for data in load_types:
            LoadType.objects.get_or_create(code=data['code'], defaults=data)

        self.stdout.write(f"Created {len(load_types)} load types.")

    def _create_container_types(self):
        container_types = [
            {
                'name': '20ft Standard',
                'length_cm': 605,
                'width_cm': 243,
                'height_cm': 259,
                'max_weight_kg': 21700,
                'volume_cubic_m': 33,
                'temperature_controlled': False
            },
            {
                'name': '40ft Standard',
                'length_cm': 1219,
                'width_cm': 243,
                'height_cm': 259,
                'max_weight_kg': 26500,
                'volume_cubic_m': 67,
                'temperature_controlled': False
            },
            {
                'name': '40ft High Cube',
                'length_cm': 1219,
                'width_cm': 243,
                'height_cm': 289,
                'max_weight_kg': 26500,
                'volume_cubic_m': 76,
                'temperature_controlled': False
            },
            {
                'name': '20ft Reefer',
                'length_cm': 605,
                'width_cm': 243,
                'height_cm': 259 ,
                'max_weight_kg': 21700,
                'volume_cubic_m': 28,
                'temperature_controlled': True
            },
            {
                'name': '40ft Reefer',
                'length_cm': 1219,
                'width_cm': 243,
                'height_cm': 259,
                'max_weight_kg': 26500,
                'volume_cubic_m': 60,
                'temperature_controlled': True
            },
            {
                'name': '20ft Flat Rack',
                'length_cm': 605,
                'width_cm': 243,
                'height_cm': 259,
                'max_weight_kg': 21700,
                'volume_cubic_m': 33,
                'temperature_controlled': False
            }
        ]

        for data in container_types: 
            ContainerType.objects.get_or_create(name=data['name'], defaults=data)

        self.stdout.write(f"Created {len(container_types)} container types.")

    def _create_freight_types(self):
        freight_types = [
            {
                'name': 'RORO',
                'description': 'Roll-on/roll-of vessels for inter-island shipping of vehicles and containerized cargo.'
            },
            {
                'name': 'Wing Van',
                'description': 'Enclosed truck with a large cargo capacity, suitable for goods requiring'
            },
            {
                'name': 'Trucking',
                'description': 'Standard land transportation for domestic shipments using Gothong\'s fleet of trucks.'
            },
            {
                'name': 'Sea Freight',
                'description': 'Ocean shipping for international cargo, using container vessels.'
            },
            {
                'name': 'Air Freight',
                'description': 'Fast transportation via aircraft, ideal for urgent or high-value shipments.'
            },
            {
                'name': 'Reefer Freight',
                'description': 'Temperature-controlled shipping for perishable goods. YelloX specializes in refrigerated transport between -20°C to +10°C.'
            },
            {
                'name': 'Specialized Trucking',
                'description': 'For hazardous materials and special handling requirements, with DENR-compliant equipment and trained personnel.'
            },
            {
                'name': 'Liquid Cargo',
                'description': 'Specialized transport for liquid goods in tankers, a specialty service offered by YelloX.'
            },
        ]

        for data in freight_types:
            FreightType.objects.get_or_create(name=data['name'], defaults=data)

        self.stdout.write(f"Created {len(freight_types)} freight types.")

    def _create_cargo_categories(self):
        cargo_categories = [
            {
                'name': 'General',
                'requires_temperature_control': False,
                'hazardous': False,
                'fragile': False,
                'special_requirements': 'Standard handling procedures apply'
            },
            {
                'name': 'Electronics',
                'requires_temperature_control': False,
                'hazardous': False,
                'fragile': True,
                'special_requirements': 'Requires anti-static packaging. ICC certification required for export shipments.'
            },
            {
                'name': 'Perishable',
                'requires_temperature_control': True,
                'hazardous': False,
                'fragile': False,
                'special_requirements': 'Requires temperature control between -20°C to +10°C depending on goods. Complies with ASEAN food safety protocols.'
            },
            {
                'name': 'Hazardous',
                'requires_temperature_control': False,
                'hazardous': True,
                'fragile': False,
                'special_requirements': 'Requires DENR AO 2019-21 compliance documentation. Minimum 3m separation from oxidizers in warehouse.'
            },
            {
                'name': 'Heavy Machinery',
                'requires_temperature_control': False,
                'hazardous': False,
                'fragile': False,
                'special_requirements': 'Requires specialized loading equipment. Weight restrictions apply.'
            },
            {
                'name': 'Liquid',
                'requires_temperature_control': False,
                'hazardous': False,
                'fragile': False,
                'special_requirements': 'Requires specialized containment to prevent leaks.'
            },
        ]  

        for data in cargo_categories:
            CargoCategory.objects.get_or_create(name=data['name'], defaults=data)

        self.stdout.write(f"Created {len(cargo_categories)} cargo categories.")