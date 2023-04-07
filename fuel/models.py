from django.db import models

# Create your models here.
class Fuel(models.Model):
    log_id = models.ForeignKey('vehicle.Log', on_delete=models.CASCADE)
    gallons = models.DecimalField(decimal_places=2, max_digits=6)
    price_gal = models.DecimalField(decimal_places=3, max_digits=8)
    total = models.DecimalField(decimal_places=3, max_digits=8)
    missed_fill = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Fuel"