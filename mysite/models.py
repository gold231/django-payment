from django.db import models
from django.contrib.auth.models import User

class Price(models.Model):
    title = models.CharField(max_length=50)
    home_area = models.CharField(max_length=50)
    monthly_price = models.IntegerField()
    onetime_price = models.IntegerField()

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
