from django.db import models

# Create your models here.
class FreightType(models.Model):
    """ Different Types of Freight services offered by Gothong Souther Group"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class ContainerType(models.Model):
    """ Container specifications """

    name = models.CharField(max_length=100) # e.g. , 20ft Standard, 40ft High Cube
    length_cm = models.FloatField()
    width_cm = models.FloatField()
    height_cm = models.FloatField()
    max_weight_kg = models.FloatField()
    volume_cubic_m = models.FloatField()
    temperature_controlled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class LoadType(models.Model):
    """ Represents the FCL, LCL, LTL load types """
    
    code = models.CharField(max_length=10) # e.g. FCL, LCL, LTL
    name = models.CharField(max_length=100) # e.g. Full Container Load and the others
    description = models.TextField()
    

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class CargoCategory(models.Model):
    """ Represents the different categories of cargos with its special handling requirements """
    name = models.CharField(max_length=100) # e.g. Electronics, Perishables, etc.
    requires_temperature_control = models.BooleanField(default=False)
    hazardous = models.BooleanField(default=False)
    fragile = models.BooleanField(default=False)
    special_requirements = models.TextField(blank=True) # e.g. "Handle with care", "Keep upright", etc.

    def __str__(self):
        return self.name
    
class FreightRecommendation(models.Model):
    """ Records of the freight recommendations made by the system """

    timestamp = models.DateTimeField(auto_now_add=True)
    cargo_weight_kg = models.FloatField()
    cargo_volume_cubic_m = models.FloatField()
    cargo_category = models.ForeignKey(CargoCategory, on_delete=models.CASCADE)
    recommended_freight_type = models.ForeignKey(FreightType, on_delete=models.CASCADE)
    recommended_container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE)
    recommended_load_type = models.ForeignKey(LoadType, on_delete=models.CASCADE)
    additional_notes = models.TextField(blank=True) # e.g. "Best for temperature-sensitive cargo", "Most cost-effective option", etc.

    def __str__(self):
        return f"Recommendation #{self.id} - {self.recommended_freight_type} ({self.recommended_load_type})"

