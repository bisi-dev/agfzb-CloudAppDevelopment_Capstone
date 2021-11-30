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

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:

    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, purchase_date, review, sentiment):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment

    def __str__(self):
        return "Dealer review: " + self.review

