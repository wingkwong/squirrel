from django.db import models
from django.urls import reverse


class Expense(models.Model):
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=1000, null=True)
    type = models.CharField(max_length=30)
    payment = models.CharField(max_length=30)
    amount = models.IntegerField()
    date = models.DateField()

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('tracker:detail', kwargs={'pk': self.pk})
