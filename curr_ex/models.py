from django.db import models

class Currency(models.Model):
    symbol = models.CharField(max_length=3)

    def __repr__(self):
        return self.symbol

class Rates(models.Model):
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE) #this is the currency we submitted
    x_currency = models.CharField(max_length=3)
    rate = models.FloatField(default=1.0)
    last_update_time = models.DateTimeField()

