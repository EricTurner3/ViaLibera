from django.db import models

# Create your models here.
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
    nickname = models.CharField(max_length=50, null=True, blank=True)
    primary_driver = models.ForeignKey('home.Person', on_delete=models.CASCADE)
    img = models.ImageField(upload_to = "static/images/vehicles/", null=True)
 
        # renames the instances of the model
        # with their title name
    def __str__(self):
        return self.nickname or str(self.year) + ' ' + self.make + ' ' + self.model
    

'''
Vehicle Specifications
Tables required to fulfill attaching specs to a vehicle
'''
class SpecificationCategory(models.Model):
    category_name = models.CharField(max_length=25)
    category_desc = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=50, default='fas fa-star')
    order = models.IntegerField(unique=True, null=True, blank=True)
 
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Specification Categories"
    
class Specification(models.Model):
    category = models.ForeignKey('SpecificationCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    units = models.CharField(max_length=10, null=True, blank=True)
 
    def __str__(self):
        return self.name
    
class VehicleSpecification(models.Model):
    specification = models.ForeignKey('Specification', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.vehicle) + ': [' + str(self.specification.category.category_name) + '] - ' + str(self.specification)
 
 # this is the master table for the vehicle. It will connect to either log, inspection result or service
# at one time, a vehicle could be in for a fillup, inspection and service at once. It will re-use the same mileage and date time.
class Log(models.Model):
    location = models.ForeignKey('home.Location', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now=True)
    mileage = models.DecimalField(decimal_places=2, max_digits=9)
    def __str__(self):
        return str(self.id) + ' - ' + str(self.dt)