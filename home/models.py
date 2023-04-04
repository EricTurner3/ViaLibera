from django.db import models
import uuid

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    license = models.CharField(max_length=50)
 
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
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
    nickname = models.CharField(max_length=50)
    primary_driver = models.ForeignKey('Person', on_delete=models.CASCADE)
    img = models.ImageField(upload_to = "images/vehicles/")
 
        # renames the instances of the model
        # with their title name
    def __str__(self):
        return self.nickname