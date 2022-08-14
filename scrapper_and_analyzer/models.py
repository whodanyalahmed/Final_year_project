from django import template
from django.db import models
import datetime
# Create your models here.


class Poll(models.Model):
    name = models.CharField(max_length=30)
    votes = models.IntegerField()

    def __str__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=80)
    price = models.IntegerField()
    website = models.CharField(max_length=80, default=None)
    image = models.CharField(max_length=80, default=None)
    link = models.CharField(max_length=80, default=None)
    fetched_date = models.DateTimeField(default=datetime.date.today)

    def __str__(self):
        return self.name + ' ' + str(self.price)
