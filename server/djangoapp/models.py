from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=1000)

    def __str__(self):
        return( "Name: " + self.name +", " \
                "Description: " + self.description )


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'SUV'
    VAN = 'Van'
    SUPERCAR = 'Supercar'
    ROADSTER = 'Roadster'
    PICKUP = 'Pickup'

    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (VAN, 'Van'),
        (SUPERCAR, 'Supercar'),
        (ROADSTER, 'Roadster'),
        (PICKUP, 'Pickup')
    ]

    name = models.CharField(null=False, max_length=30)
    carType = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SUV
    )
    year = models.DateField()
    dealerId = models.IntegerField(default=0)
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return( "Name: " + self.name + ", " \
                # "Car make: " + self.carMake + ", " \
                "Type: " + self.carType + ", " \
        )
        # return ("foo")

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    # def __init__(self, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.dealership = kwargs['dealership']
        self.review = kwargs['review']
        if 'purchase' in kwargs:
            self.purchase = kwargs['purchase']
            if kwargs['purchase'] == 'true':
                self.purchase_date = kwargs['purchase_date']
                self.car_make = kwargs['car_make']
                self.car_model = kwargs['car_model']
                self.car_year = kwargs['car_year']
        self.sentiment = kwargs['sentiment']

    def __str__(self):
        return self.name + ": " + self.review