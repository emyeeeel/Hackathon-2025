from django.contrib import admin
from backend.api.models import Box, PackedBox, Product

# Register your models here.
admin.site.register(Product)
admin.site.register(Box)
admin.site.register(PackedBox)
