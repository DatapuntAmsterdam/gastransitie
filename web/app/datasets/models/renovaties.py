from django.contrib.gis.db import models

class Renovatie(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    buurt = models.CharField(max_length=4, blank=True, null=True)
    alliantie = models.IntegerField(blank=True, null=True)
    de_key = models.IntegerField(blank=True, null=True)
    eigen_haar = models.IntegerField(blank=True, null=True)
    rochdale = models.IntegerField(blank=True, null=True)
    stadgenoot = models.IntegerField(blank=True, null=True)
    ymere = models.IntegerField(blank=True, null=True)
    eindtotaal = models.IntegerField(blank=True, null=True)
    jaar_2017 = models.IntegerField(blank=True, null=True)
    jaar_2018 = models.IntegerField(blank=True, null=True)
    jaar_2019 = models.IntegerField(blank=True, null=True)
    jaar_2020 = models.IntegerField(blank=True, null=True)
    jaar_2021 = models.IntegerField(blank=True, null=True)
    jaar_2022 = models.IntegerField(blank=True, null=True)
    jaar_2023 = models.IntegerField(blank=True, null=True)
    jaar_onbekend = models.IntegerField(blank=True, null=True)
    wkb_geometry = models.PolygonField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'renovaties_clean'
