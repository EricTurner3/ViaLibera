from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    license = models.CharField(max_length=50, null=True)
 
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    class Meta:
        verbose_name_plural = "people"
    

class Location(models.Model):
    name = models.CharField(max_length=25)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=25)
    postal = models.IntegerField()
 
    def __str__(self):
        return self.name
    




