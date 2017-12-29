from django.contrib.gis.db import models


class CBSBuurt(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    bu_code = models.CharField(max_length=10, blank=True, null=True)
    bu_naam = models.CharField(max_length=60, blank=True, null=True)
    wk_code = models.CharField(max_length=8, blank=True, null=True)
    gm_code = models.CharField(max_length=6, blank=True, null=True)
    gm_naam = models.CharField(max_length=60, blank=True, null=True)
    ind_wbi = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    water = models.CharField(max_length=4, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    dek_perc = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    oad = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    sted = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    aant_inw = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    aant_man = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    aant_vrouw = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_00_14_jr = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_15_24_jr = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_25_44_jr = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_45_64_jr = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_65_eo_jr = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_ongehuwd = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_gehuwd = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_gescheid = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_verweduw = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    bev_dichth = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    aantal_hh = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_eenp_hh = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_hh_z_k = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_hh_m_k = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    gem_hh_gr = models.DecimalField(
        max_digits=11, decimal_places=1, blank=True, null=True)
    p_west_al = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_n_w_al = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_marokko = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_ant_aru = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_surinam = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_turkije = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    p_over_nw = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    opp_tot = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    opp_land = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    opp_water = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gas_cbs_buurt_2017_raw'
        verbose_name = 'CBS buurt'
        verbose_name_plural = 'CBS buurten'

    def __str__(self):
        if self.bu_naam:
            return '{} - {}'.format(self.bu_naam, self.bu_code)
        else:
            return '{}'.format(self.bu_code)
