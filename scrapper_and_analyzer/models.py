from django import template
from django.db import models

# Create your models here.


class Poll(models.Model):
    name = models.CharField(max_length=30)
    votes = models.IntegerField()

    def __str__(self):
        return self.name
