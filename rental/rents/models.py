from django.db import models
from django.conf import settings


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

    def __str__(self):
        return self.get_frequently_display()


# Create your models here.
class Rentals(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='rent_user', null=True)
    neto_price = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True)
    familiar_rental_promotion = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'rents'
        db_table = 'rentals'

    def __str__(self):
        return self.user.username


class Bike(models.Model):

    rentals = models.ForeignKey(Rentals, related_name="rentals_bike")
    price_by_frecuency = models.ForeignKey(
        PriceByFrecuency, related_name="price_bike")
    quantity = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'rents'
        db_table = 'bike'

    def __str__(self):
        return str(self.create_at)
