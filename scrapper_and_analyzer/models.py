from django import template
from django.db import models

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

    def __str__(self):
        return self.name + ' ' + str(self.price)
