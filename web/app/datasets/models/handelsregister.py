
from django.contrib.gis.db import models

from django.contrib.postgres.fields import JSONField

from datasets.models import bag


class Handelsregister(models.Model):
    """
    HR summary information for each neighborhood
    """

    buurt_id = models.CharField(max_length=14)
    buurt_naam = models.CharField(max_length=40)
    data = JSONField()
