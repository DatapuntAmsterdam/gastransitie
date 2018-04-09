from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField


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


class VerbruikPerBuurt(models.Model):
    id = models.CharField(max_length=14, primary_key=True)
    code = models.CharField(max_length=3)
    vollcode = models.CharField(max_length=4)
    naam = models.CharField(max_length=40)
    data = JSONField()


class AllianderKv(models.Model):
    index = models.BigIntegerField(primary_key=True)
    meetverantwoordelijke = models.TextField(db_column='MEETVERANTWOORDELIJKE', blank=True, null=True)  # Field name made lowercase.
    netbeheerder = models.TextField(db_column='NETBEHEERDER', blank=True, null=True)  # Field name made lowercase.
    netgebied = models.TextField(db_column='NETGEBIED', blank=True, null=True)  # Field name made lowercase.
    straatnaam = models.TextField(db_column='STRAATNAAM', blank=True, null=True)  # Field name made lowercase.
    postcode_van = models.TextField(db_column='POSTCODE_VAN', blank=True, null=True)  # Field name made lowercase.
    postcode_tot = models.TextField(db_column='POSTCODE_TOT', blank=True, null=True)  # Field name made lowercase.
    woonplaats = models.TextField(db_column='WOONPLAATS', blank=True, null=True)  # Field name made lowercase.
    landcode = models.TextField(db_column='LANDCODE', blank=True, null=True)  # Field name made lowercase.
    productsoort = models.TextField(db_column='PRODUCTSOORT', blank=True, null=True)  # Field name made lowercase.
    verbruikssegment = models.TextField(db_column='VERBRUIKSSEGMENT', blank=True, null=True)  # Field name made lowercase.
    aantal_aansluitingen = models.FloatField(db_column='Aantal Aansluitingen', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    leveringsrichting = models.FloatField(db_column='Leveringsrichting', blank=True, null=True)  # Field name made lowercase.
    fysieke_status = models.FloatField(db_column='Fysieke status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    defintieve_aansl_nrm_field = models.FloatField(db_column='Defintieve aansl  NRM ', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    soort_aansluiting = models.FloatField(db_column='Soort aansluiting', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    soort_aansluiting_naam = models.TextField(db_column='Soort aansluiting Naam', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sjv = models.FloatField(db_column='SJV', blank=True, null=True)  # Field name made lowercase.
    sjv_laag_tarief = models.FloatField(db_column='SJV laag tarief', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    slimme_meter = models.FloatField(db_column='Slimme Meter', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gemiddeld_aantal_telwielen = models.TextField(db_column='Gemiddeld aantal telwielen', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'alliander_kv'
