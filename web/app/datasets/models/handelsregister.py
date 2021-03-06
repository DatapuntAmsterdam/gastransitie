from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

# from datasets.models import bag


class Handelsregister(models.Model):
    """HR summary information for each neighbourhood

    Stores CSV download data from dataselectie
    of all vestigingen and maatschappelijke activiteiten
    from Dataselectie API.
    """
    buurt_id = models.CharField(max_length=14)
    buurt_naam = models.CharField(max_length=40)
    data = JSONField()


class SBIcodes(models.Model):
    """SBI codes from cbs.
    """

    code = models.CharField(
        max_length=8,
        primary_key=True
    )

    title = models.TextField()

    sbi_tree = JSONField()
    qa_tree = JSONField(null=True)


class HandelsregisterBuurt(models.Model):
    """Summary Information for each buurt

    Stores a aggegated HR summary rapport of all
    vestigingen and activiteiten in a neighbourhood.
    """
    buurt_id = models.CharField(max_length=14)
    buurt_naam = models.CharField(max_length=40)
    data = JSONField()
