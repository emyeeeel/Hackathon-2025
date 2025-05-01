from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD_GRADE', 'Food Grade'),
        ('GENERAL', 'General Goods'),
        ('ENDANGERED', 'Endangered Goods'),
    ]
    
    SUBCATEGORY_CHOICES = [
        ('ELECTRONICS', 'Electronics & Accessories'),
        ('KITCHEN', 'Small Kitchen Appliances'),
        ('PERSONAL_CARE', 'Personal Care & Cosmetics'),
        ('APPAREL', 'Apparel & Accessories'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=20, choices=SUBCATEGORY_CHOICES)
    width = models.DecimalField(max_digits=6, decimal_places=2)  # in cm
    height = models.DecimalField(max_digits=6, decimal_places=2)  # in cm
    length = models.DecimalField(max_digits=6, decimal_places=2)  # in cm
    weight = models.DecimalField(max_digits=6, decimal_places=2)  # in kg
    quantity = models.PositiveIntegerField(default=1)  # Default quantity is 1
    is_fragile = models.BooleanField(default=False)
    requires_refrigeration = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_weight(self):
        return self.weight * self.quantity

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    

class Box(models.Model):
    name = models.CharField(max_length=200)
    length = models.DecimalField(max_digits=6, decimal_places=2)  # in cm
    width = models.DecimalField(max_digits=6, decimal_places=2)  # in cm
    height = models.DecimalField(max_digits=6, decimal_places=2)  # in cm
    weight = models.DecimalField(max_digits=6, decimal_places=2)  # in kg
    fill_capacity = models.DecimalField(max_digits=6, decimal_places=2)  # in kg
    volume = models.DecimalField(max_digits=10, decimal_places=2)  # in cm^3

    def __str__(self):
        return self.name