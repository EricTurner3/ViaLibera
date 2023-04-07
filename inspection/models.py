from django.db import models

# Create your models here.
class InspectionCategory(models.Model):
    category_name = models.CharField(max_length=25)
    category_desc = models.CharField(max_length=100, null=True, default=None)
 
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Inspection Categories"
    
class InspectionTask(models.Model):
    category_id = models.ForeignKey('InspectionCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    desc_simple = models.CharField(max_length=255)
    desc_detailed = models.TextField()
    unit = models.CharField(max_length=10)
    has_status = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    
class InspectionStatus(models.Model):
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    index = models.IntegerField(unique=True) # Sets the order of the statuses
 
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Inspection Statuses"
    
class Inspection(models.Model):
    inspector_id = models.ForeignKey('home.Person', on_delete=models.CASCADE)
    log_id = models.ForeignKey('vehicle.Log', on_delete=models.CASCADE)
    summary = models.TextField()
    
class InspectionResult(models.Model):
    inspection_id = models.ForeignKey('Inspection', on_delete=models.CASCADE)
    task_id = models.ForeignKey('InspectionTask', on_delete=models.CASCADE)
    status_id = models.ForeignKey('InspectionStatus', on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=50)
    skipped = models.BooleanField(default=False)
    notes = models.TextField()