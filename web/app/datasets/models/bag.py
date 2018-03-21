"""
Models for restored database tables (from BAG imports).
"""
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField


class BagBuurt(models.Model):
    id = models.CharField(max_length=14, primary_key=True)
    code = models.CharField(max_length=3)
    vollcode = models.CharField(max_length=4)
    naam = models.CharField(max_length=40)
    vervallen = models.NullBooleanField()
    ingang_cyclus = models.DateField(blank=True, null=True)
    brondocument_naam = models.CharField(max_length=100, blank=True, null=True)
    brondocument_datum = models.DateField(blank=True, null=True)
    stadsdeel_id = models.CharField(max_length=14)
    buurtcombinatie_id = models.CharField(max_length=14, blank=True, null=True)

    date_modified = models.DateTimeField()
    begin_geldigheid = models.DateField(blank=True, null=True)
    einde_geldigheid = models.DateField(blank=True, null=True)
    geometrie = models.MultiPolygonField(srid=28992, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bag_buurt'


class BagRapport(models.Model):
    id = models.CharField(max_length=14, primary_key=True)
    code = models.CharField(max_length=3)
    vollcode = models.CharField(max_length=4)
    naam = models.CharField(max_length=40)
    data = JSONField()
