from django.contrib.gis import admin
from datasets.models import GasAfwc2017
from datasets.models import CBSBuurt


class NoEditMixin():
    """
    Disable editing models (in UI) without 403s.

    Note: define has_change_permission method to cause 403 errors.
    """
    modifiable = False
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, extra_context=None):
        # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.change_view
        # see: django/contrib/admin/templatetags/admin_modify.py
        # see: django/contrib/admin/templates/admin/submit_line.html
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_delete'] = False
        extra_context['save_as'] = False
        extra_context['show_save_and_continue'] = False

        return super().change_view(
            request, object_id, extra_context=extra_context)


class GasAfwc2017Admin(NoEditMixin, admin.ModelAdmin):
    readonly_fields = (
        'ogc_fid',
        'corp',
        'corporatie',
        'bouwjaar',
        'aantal_adressen',
        'aantal_corporatie',
        'percentage_corporatie',
        'gemeente',
        'perc',
    )


class CBSBuurtAdmin(NoEditMixin, admin.ModelAdmin):
    readonly_fields = (
        'ogc_fid',
        'bu_code',
        'bu_naam',
        'wk_code',
        'gm_code',
        'gm_naam',
        'ind_wbi',
        'water',
        'postcode',
        'dek_perc',
        'oad',
        'sted',
        'aant_inw',
        'aant_man',
        'aant_vrouw',
        'p_00_14_jr',
        'p_15_24_jr',
        'p_25_44_jr',
        'p_45_64_jr',
        'p_65_eo_jr',
        'p_ongehuwd',
        'p_gehuwd',
        'p_gescheid',
        'p_verweduw',
        'bev_dichth',
        'aantal_hh',
        'p_eenp_hh',
        'p_hh_z_k',
        'p_hh_m_k',
        'gem_hh_gr',
        'p_west_al',
        'p_n_w_al',
        'p_marokko',
        'p_ant_aru',
        'p_surinam',
        'p_turkije',
        'p_over_nw',
        'opp_tot',
        'opp_land',
        'opp_water',
    )


admin.site.register(GasAfwc2017, GasAfwc2017Admin)
admin.site.register(CBSBuurt, CBSBuurtAdmin)
admin.site.site_header = 'Energietransitie project admin'
