from django.contrib import admin
from .models import FreightType, ContainerType, LoadType, CargoCategory, FreightRecommendation

# Register your models here.

admin.site.register(FreightType)
admin.site.register(ContainerType)
admin.site.register(LoadType)
admin.site.register(CargoCategory)
admin.site.register(FreightRecommendation)
