from django.db import models

class MedianPrice(models.Model):
    name = models.CharField(max_length=100, null=False)
    state_code = models.CharField(max_length=2, null=False)
    list_price = models.IntegerField()