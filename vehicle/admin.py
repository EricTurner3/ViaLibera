from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Vehicle)
admin.site.register(SpecificationCategory)
admin.site.register(Specification)
admin.site.register(VehicleSpecification)