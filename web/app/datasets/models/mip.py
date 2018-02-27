from django.contrib.gis.db import models


class Mip2016(models.Model):
    """
    Meerjarig Investerings Programma
    """
    ogc_fid = models.IntegerField(primary_key=True)
    datum = models.CharField(max_length=255, blank=True, null=True)
    organisatie = models.CharField(max_length=255, blank=True, null=True)
    opdrachtgever = models.CharField(max_length=255, blank=True, null=True)
    nummer = models.CharField(max_length=255, blank=True, null=True)
    omschrijving = models.CharField(max_length=255, blank=True, null=True)
    wkb_geometry = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mip2016_clean'
