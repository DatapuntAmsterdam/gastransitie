# import random
import string
from datetime import datetime
import pytz

# import faker
import factory
# import pytz
# from django.contrib.gis.geos import Point
from factory import fuzzy

from datasets.models.corporatie_bezit import GasAfwc2017
from datasets.models.bag import BagRapport
from datasets.models.bag import BagBuurt
from datasets.models.cbs import CBSBuurt
from datasets.models.mip import Mip2016
from datasets.models.energie_labels import EnergieLabel
from datasets.models.renovaties import Renovatie
from datasets.models.handelsregister import Handelsregister
#  from datasets.models.handelsregister import SBIcodes
from datasets.models.handelsregister import HandelsregisterBuurt


class RenovatieFactory(factory.DjangoModelFactory):

    class Meta:
        model = Renovatie

    ogc_fid = fuzzy.FuzzyInteger(low=0)
    alliantie = fuzzy.FuzzyInteger(low=0)
    de_key = fuzzy.FuzzyInteger(low=0)
    eigen_haar = fuzzy.FuzzyInteger(low=0)
    rochdale = fuzzy.FuzzyInteger(low=0)
    stadgenoot = fuzzy.FuzzyInteger(low=0)
    ymere = fuzzy.FuzzyInteger(low=0)
    eindtotaal = fuzzy.FuzzyInteger(low=0)
    jaar_2017 = fuzzy.FuzzyInteger(low=0)
    jaar_2018 = fuzzy.FuzzyInteger(low=0)
    jaar_2019 = fuzzy.FuzzyInteger(low=0)
    jaar_2020 = fuzzy.FuzzyInteger(low=0)
    jaar_2021 = fuzzy.FuzzyInteger(low=0)
    jaar_2022 = fuzzy.FuzzyInteger(low=0)
    jaar_2023 = fuzzy.FuzzyInteger(low=0)
    jaar_onbekend = fuzzy.FuzzyInteger(low=0)
    # wkb_geometry = models.PolygonField(blank=True, null=True)
    # wkb_geometry = fuzzy.GeometryField()


class BuurtFactory(factory.DjangoModelFactory):
    class Meta:
        model = BagBuurt
        django_get_or_create = ('code',)

    id = fuzzy.FuzzyText(length=14, chars=string.digits)
    code = fuzzy.FuzzyText(length=3, chars=string.digits)
    stadsdeel_id = fuzzy.FuzzyText(length=14, chars=string.digits)
    buurtcombinatie_id = fuzzy.FuzzyText(length=4)
    date_modified = fuzzy.FuzzyDateTime(
       datetime(2008, 1, 1, 0, tzinfo=pytz.UTC))


class CBSBuurtFactory(factory.DjangoModelFactory):
    class Meta:
        model = CBSBuurt

    bu_code = fuzzy.FuzzyText(length=10)
    bu_naam = fuzzy.FuzzyText(length=60)
    wk_code = fuzzy.FuzzyText(length=8)
    gm_code = fuzzy.FuzzyText(length=6)
    gm_naam = fuzzy.FuzzyText(length=60)


class GasAfwc2017Factory(factory.DjangoModelFactory):
    class Meta:
        model = GasAfwc2017

    ogc_fid = fuzzy.FuzzyInteger(low=0)
    corp = fuzzy.FuzzyText(length=255)
    corporatie = fuzzy.FuzzyText(length=255)
    bouwjaar = fuzzy.FuzzyInteger(low=0)
    aantal_adressen = fuzzy.FuzzyInteger(low=0)
    aantal_corporatie = fuzzy.FuzzyInteger(low=0)
    percentage_corporatie = fuzzy.FuzzyInteger(low=0)
    gemeente = fuzzy.FuzzyText()
    perc = fuzzy.FuzzyInteger(low=0)
    # wkb_geometry = fuzzy.GeometryField()


class Mip2016Factory(factory.DjangoModelFactory):

    class Meta:
        model = Mip2016

    ogc_fid = fuzzy.FuzzyInteger(low=0)
    datum = fuzzy.FuzzyText(length=255)
    organisatie = fuzzy.FuzzyText(length=255)
    opdrachtgever = fuzzy.FuzzyText(length=255)
    nummer = fuzzy.FuzzyText(length=255)
    omschrijving = fuzzy.FuzzyText(length=255)
    # wkb_geometry = fuzzy.GeometryField()


class BagRapportFactory(factory.DjangoModelFactory):
    """
    Contains json doc with information about owners ship and
    other counts
    """

    class Meta:
        model = BagRapport

    id = fuzzy.FuzzyText(length=14)
    code = fuzzy.FuzzyText(length=3)
    vollcode = fuzzy.FuzzyText(length=4)
    naam = fuzzy.FuzzyText(length=40)
    data = dict(empty=True)


class EnergieLabelFactory(factory.DjangoModelFactory):

    class Meta:
        model = EnergieLabel

    ogc_fid = fuzzy.FuzzyInteger(low=0)
    energielabel = fuzzy.FuzzyText(length=1)
    # wkb_geometry = fuzzy.GeometryField()


class HandelsregisterBuurtFactory(factory.DjangoModelFactory):

    class Meta:
        model = HandelsregisterBuurt

    buurt_id = fuzzy.FuzzyText(length=14, chars=string.digits)
    buurt_naam = fuzzy.FuzzyText(length=40)
    data = dict(empty=True)


class HandelsregisterFactory(factory.DjangoModelFactory):

    class Meta:
        model = Handelsregister

    buurt_id = fuzzy.FuzzyText(length=14, chars=string.digits)
    buurt_naam = fuzzy.FuzzyText(length=40)
    data = dict(empty=True)
