from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)
    license_plate = models.CharField(max_length=20)
    gas_tank_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    oil_capacity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    transmission_fluid_capacity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    coolant_capacity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    brake_fluid_capacity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    current_mileage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    class Meta:
        ordering = ['-year', 'make', 'model']

class FuelRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_records')
    date = models.DateTimeField()
    mileage = models.IntegerField()
    gallons = models.DecimalField(max_digits=5, decimal_places=2)
    cost_per_gallon = models.DecimalField(max_digits=5, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate total cost
        self.total_cost = self.gallons * self.cost_per_gallon
        # Update vehicle's current mileage
        self.vehicle.current_mileage = self.mileage
        self.vehicle.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Fuel Record - {self.vehicle} - {self.date}"

    class Meta:
        ordering = ['-date']

class ServiceRecord(models.Model):
    SERVICE_TYPES = [
        ('Oil Change', 'Oil Change'),
        ('Tire Rotation', 'Tire Rotation'),
        ('Brake Service', 'Brake Service'),
        ('Transmission Service', 'Transmission Service'),
        ('Coolant Flush', 'Coolant Flush'),
        ('Air Filter', 'Air Filter'),
        ('Battery', 'Battery'),
        ('Other', 'Other')
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='service_records')
    date = models.DateTimeField()
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    mileage = models.IntegerField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Update vehicle's current mileage
        self.vehicle.current_mileage = self.mileage
        self.vehicle.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service_type} - {self.vehicle} - {self.date}"

    class Meta:
        ordering = ['-date']
