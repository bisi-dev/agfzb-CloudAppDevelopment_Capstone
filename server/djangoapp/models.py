from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return self.name + " " + self.description    

class CarModel(models.Model):
    carmake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    dealer_id = models.IntegerField(null=False)

    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'

    CAR_TYPES = [
        (SEDAN,'Sedan'),
        (SUV,'SUV'),
        (WAGON,'WAGON')
    ]

    car_type = models.CharField(max_length=5, choices=CAR_TYPES)
    year = models.DateField(null=False)

    def __str__(self):
        return self.name + " " + str(self.car_type)+" "+str(self.year)




# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
