from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Vote(models.Model):
    ip_address = models.CharField(max_length=45)
    date = models.DateField(auto_now_add=True)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE,
                                   related_name='votes')
    weight = models.DecimalField(default=0, max_digits=3, decimal_places=2)

    def __str__(self):
        return self.restaurant.name
