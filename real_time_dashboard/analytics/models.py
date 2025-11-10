from django.db import models

# Create your models here.


class StockData(models.Model):
    symbol = models.CharField(max_length=20)
    price = models.FloatField()
    volume = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
