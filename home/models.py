from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    license = models.CharField(max_length=50, null=True)
 
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    class Meta:
        verbose_name_plural = "people"
    
class Vehicle(models.Model):
    # uses actual name unless there were spaces or spec chars
    manufacturers = [
        ("Abarth", "Abarth"),
        ("AR", "Alfa Romeo"),
        ("AM", "Aston Martin"),
        ("Audi", "Audi"),
        ("Bentley", "Bentley"),
        ("BMW", "BMW"),
        ("Bugatti", "Bugatti"),
        ("Cadillac", "Cadillac"),
        ("Chevrolet", "Chevrolet"),
        ("Chrysler", "Chrysler"),
        ("Citroen", "Citroën"),
        ("Dacia", "Dacia"),
        ("Daewoo", "Daewoo"),
        ("Daihatsu", "Daihatsu"),
        ("Dodge", "Dodge"),
        ("Donkervoort", "Donkervoort"),
        ("DS", "DS"),
        ("Ferrari", "Ferrari"),
        ("Fiat", "Fiat"),
        ("Fisker", "Fisker"),
        ("Ford", "Ford"),
        ("Honda", "Honda"),
        ("Hummer", "Hummer"),
        ("Hyundai", "Hyundai"),
        ("Infiniti", "Infiniti"),
        ("Iveco", "Iveco"),
        ("Jaguar", "Jaguar"),
        ("Jeep", "Jeep"),
        ("Kia", "Kia"),
        ("KTM", "KTM"),
        ("Lada", "Lada"),
        ("Lamborghini", "Lamborghini"),
        ("Lancia", "Lancia"),
        ("Land Rover", "Land Rover"),
        ("Landwind", "Landwind"),
        ("Lexus", "Lexus"),
        ("Lotus", "Lotus"),
        ("Maserati", "Maserati"),
        ("Maybach", "Maybach"),
        ("Mazda", "Mazda"),
        ("McLaren", "McLaren"),
        ("MB", "Mercedes-Benz"),
        ("MG", "MG"),
        ("Mini", "Mini"),
        ("Mitsubishi", "Mitsubishi"),
        ("Morgan", "Morgan"),
        ("Nissan", "Nissan"),
        ("Opel", "Opel"),
        ("Peugeot", "Peugeot"),
        ("Porsche", "Porsche"),
        ("Renault", "Renault"),
        ("RR", "Rolls-Royce"),
        ("Rover", "Rover"),
        ("Saab", "Saab"),
        ("Seat", "Seat"),
        ("Skoda", "Skoda"),
        ("Smart", "Smart"),
        ("SsangYong", "SsangYong"),
        ("Subaru", "Subaru"),
        ("Suzuki", "Suzuki"),
        ("Tesla", "Tesla"),
        ("Toyota", "Toyota"),
        ("Volkswagen", "Volkswagen"),
        ("Volvo", "Volvo"),

    ]
    year = models.IntegerField()
    make = models.CharField(max_length=25, choices=manufacturers, default="Abarth")
    model = models.CharField(max_length=100)
    vin = models.CharField(max_length=18)
    nickname = models.CharField(max_length=50, null=True)
    primary_driver = models.ForeignKey('Person', on_delete=models.CASCADE)
    img = models.ImageField(upload_to = "static/images/vehicles/", null=True)
 
        # renames the instances of the model
        # with their title name
    def __str__(self):
        return self.nickname
    

'''
Vehicle Specifications
Tables required to fulfill attaching specs to a vehicle
'''
class SpecificationCategory(models.Model):
    category_name = models.CharField(max_length=25)
    category_desc = models.CharField(max_length=100, null=True)
 
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Specification Categories"
    
class Specification(models.Model):
    category_id = models.ForeignKey('SpecificationCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    units = models.CharField(max_length=10, null=True)
 
    def __str__(self):
        return self.name
    
class VehicleSpecification(models.Model):
    specification_id = models.ForeignKey('Specification', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True)
 
'''
Maintenance / Fuel Logs
Tables required to fulfill attaching logs to a vehicle
'''
class Location(models.Model):
    name = models.CharField(max_length=25)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=25)
    postal = models.IntegerField()
 
    def __str__(self):
        return self.name
    
# this is the master table for the vehicle. It will connect to either log, inspection result or service
# at one time, a vehicle could be in for a fillup, inspection and service at once. It will re-use the same mileage and date time.
class Log(models.Model):
    location_id = models.ForeignKey('Location', on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now=True)
    mileage = models.DecimalField(decimal_places=2, max_digits=9)
    def __str__(self):
        return str(self.id) + ' - ' + str(self.dt)

class Fuel(models.Model):
    log_id = models.ForeignKey('Log', on_delete=models.CASCADE)
    gallons = models.DecimalField(decimal_places=2, max_digits=6)
    price_gal = models.DecimalField(decimal_places=3, max_digits=8)
    total = models.DecimalField(decimal_places=3, max_digits=8)
    missed_fill = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Fuel"

class Maintenance(models.Model):
    name = models.CharField(max_length=25)
    desc = models.CharField(max_length=100, null=True, default=None)
 
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Maintenance"
    
class Service(models.Model):
    log_id = models.ForeignKey('Log', on_delete=models.CASCADE)
    maintenance_id = models.ForeignKey('Maintenance', on_delete=models.CASCADE)
    cost = models.DecimalField(decimal_places=2, max_digits=8)
    comment = models.CharField(max_length=100, null=True, default=None)

'''
Inspection Tables
Tables required to fulfill attaching inspection information to a log
'''
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
    inspector_id = models.ForeignKey('Person', on_delete=models.CASCADE)
    log_id = models.ForeignKey('Log', on_delete=models.CASCADE)
    summary = models.TextField()
    
class InspectionResult(models.Model):
    inspection_id = models.ForeignKey('Inspection', on_delete=models.CASCADE)
    task_id = models.ForeignKey('InspectionTask', on_delete=models.CASCADE)
    status_id = models.ForeignKey('InspectionStatus', on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=50)
    skipped = models.BooleanField(default=False)
    notes = models.TextField()