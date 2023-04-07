from django.db import models

# Create your models here.
class Maintenance(models.Model):
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=100, null=True, default=None)
 
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Maintenance"
    
class Service(models.Model):
    log_id = models.ForeignKey('vehicle.Log', on_delete=models.CASCADE)
    maintenance_id = models.ForeignKey('Maintenance', on_delete=models.CASCADE)
    cost = models.DecimalField(decimal_places=2, max_digits=8)
    comment = models.CharField(max_length=100, null=True, default=None)

