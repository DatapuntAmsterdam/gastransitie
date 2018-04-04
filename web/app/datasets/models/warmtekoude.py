from django.contrib.gis.db import models


class Warmtekoude(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    type_net = models.CharField(max_length=255, blank=True, null=True)
    eigenaar_net = models.CharField(max_length=255, blank=True, null=True)
    soort_leiding = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    selectie = models.CharField(max_length=255, blank=True, null=True)
    filter = models.CharField(max_length=255, blank=True, null=True)
    wkb_geometry = models.LineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warmtekoude_clean'


class WarmtekoudeSimple(models.Model):
    selectie = models.CharField(max_length=255, blank=True, null=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wk_merged_buff'
        # db_table = 'wk_merged_grid'
