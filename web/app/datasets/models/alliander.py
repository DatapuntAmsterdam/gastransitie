from django.contrib.gis.db import models


class GasGroen(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    id = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    shape_leng = models.DecimalField(
        max_digits=19, decimal_places=11, blank=True, null=True)
    ruleid = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gas_alliander_gas_groen_raw'


class GasOranje(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    objectid = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    id = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    shape_leng = models.DecimalField(
        max_digits=19, decimal_places=11, blank=True, null=True)
    ruleid = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    wkb_geometry = models.LineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gas_alliander_gas_oranje_raw'
