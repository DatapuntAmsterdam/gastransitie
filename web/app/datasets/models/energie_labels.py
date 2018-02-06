from django.contrib.gis.db import models


class EnergieLabel(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    energielabel = models.CharField(max_length=1, blank=True, null=True)
    wkb_geometry = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'energie_labels_clean'
