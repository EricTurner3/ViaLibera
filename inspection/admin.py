from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(InspectionCategory)
admin.site.register(InspectionTask)
admin.site.register(InspectionStatus)
admin.site.register(Inspection)
admin.site.register(InspectionResult)