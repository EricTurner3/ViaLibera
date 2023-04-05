from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Person)
admin.site.register(Vehicle)
admin.site.register(SpecificationCategory)
admin.site.register(Specification)
admin.site.register(VehicleSpecification)
admin.site.register(Location)
admin.site.register(Log)
admin.site.register(Fuel)
admin.site.register(Maintenance)
admin.site.register(Service)
admin.site.register(InspectionCategory)
admin.site.register(InspectionTask)
admin.site.register(InspectionStatus)
admin.site.register(Inspection)
admin.site.register(InspectionResult)