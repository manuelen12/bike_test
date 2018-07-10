from django.db import models


class PriceByFrecuency(models.Model):
    __frequently = (
        (2, "Daily"),
        (3, "weekly"),
        (1, "Hourly"),
    )
    frequently = models.SmallIntegerField(
        default=1, choices=__frequently)
    price = models.IntegerField()

    class Meta:
        app_label = 'rents'
        db_table = 'price_by_frecuency'


# Create your models here.
class Rentals(models.Model):

    neto_price = models.IntegerField(null=True)
    familiar_rental_promotion = models.BooleanField(default=False)
    total_price = models.FloatField(null=True)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'rents'
        db_table = 'rentals'


class Bike(models.Model):

    rentals = models.ForeignKey(Rentals, related_name="rentals_bike")
    price_by_frecuency = models.ForeignKey(
        PriceByFrecuency, related_name="price_bike")
    quantity = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'rents'
        db_table = 'bike'
