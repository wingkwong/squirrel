from django.db import models


class Expense(models.Model):
    currency = models.CharField(max_length=3)
    description = models.CharField(mxa_length=1000, null=True)
    type = models.CharField(max_length=30)
    payment = models.CharField(max_length=30)
    amount = models.IntegerField()
    date = models.DateField()
