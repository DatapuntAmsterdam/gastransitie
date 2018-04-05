# Generated by Django 2.0.2 on 2018-04-05 13:50

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0005_bagrapport'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllianderKv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField(blank=True, null=True)),
                ('meetverantwoordelijke', models.TextField(blank=True, db_column='MEETVERANTWOORDELIJKE', null=True)),
                ('netbeheerder', models.TextField(blank=True, db_column='NETBEHEERDER', null=True)),
                ('netgebied', models.TextField(blank=True, db_column='NETGEBIED', null=True)),
                ('straatnaam', models.TextField(blank=True, db_column='STRAATNAAM', null=True)),
                ('postcode_van', models.TextField(blank=True, db_column='POSTCODE_VAN', null=True)),
                ('postcode_tot', models.TextField(blank=True, db_column='POSTCODE_TOT', null=True)),
                ('woonplaats', models.TextField(blank=True, db_column='WOONPLAATS', null=True)),
                ('landcode', models.TextField(blank=True, db_column='LANDCODE', null=True)),
                ('productsoort', models.TextField(blank=True, db_column='PRODUCTSOORT', null=True)),
                ('verbruikssegment', models.TextField(blank=True, db_column='VERBRUIKSSEGMENT', null=True)),
                ('aantal_aansluitingen', models.FloatField(blank=True, db_column='Aantal Aansluitingen', null=True)),
                ('leveringsrichting', models.FloatField(blank=True, db_column='Leveringsrichting', null=True)),
                ('fysieke_status', models.FloatField(blank=True, db_column='Fysieke status', null=True)),
                ('defintieve_aansl_nrm_field', models.FloatField(blank=True, db_column='Defintieve aansl  NRM ', null=True)),
                ('soort_aansluiting', models.FloatField(blank=True, db_column='Soort aansluiting', null=True)),
                ('soort_aansluiting_naam', models.TextField(blank=True, db_column='Soort aansluiting Naam', null=True)),
                ('sjv', models.FloatField(blank=True, db_column='SJV', null=True)),
                ('sjv_laag_tarief', models.FloatField(blank=True, db_column='SJV laag tarief', null=True)),
                ('slimme_meter', models.FloatField(blank=True, db_column='Slimme Meter', null=True)),
                ('gemiddeld_aantal_telwielen', models.TextField(blank=True, db_column='Gemiddeld aantal telwielen', null=True)),
            ],
            options={
                'db_table': 'alliander_kv',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GasGroen',
            fields=[
                ('ogc_fid', models.AutoField(primary_key=True, serialize=False)),
                ('objectid', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('id', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('shape_leng', models.DecimalField(blank=True, decimal_places=11, max_digits=19, null=True)),
                ('ruleid', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'gas_alliander_gas_groen_raw',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GasOranje',
            fields=[
                ('ogc_fid', models.AutoField(primary_key=True, serialize=False)),
                ('objectid', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('id', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('shape_leng', models.DecimalField(blank=True, decimal_places=11, max_digits=19, null=True)),
                ('ruleid', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'gas_alliander_gas_oranje_raw',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Warmtekoude',
            fields=[
                ('ogc_fid', models.IntegerField(primary_key=True, serialize=False)),
                ('type_net', models.CharField(blank=True, max_length=255, null=True)),
                ('eigenaar_net', models.CharField(blank=True, max_length=255, null=True)),
                ('soort_leiding', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('selectie', models.CharField(blank=True, max_length=255, null=True)),
                ('filter', models.CharField(blank=True, max_length=255, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'warmtekoude_clean',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WarmtekoudeSimple',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selectie', models.CharField(blank=True, max_length=255, null=True)),
                ('wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'wk_merged_buff',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VerbruikPerBuurt',
            fields=[
                ('id', models.CharField(max_length=14, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=3)),
                ('vollcode', models.CharField(max_length=4)),
                ('naam', models.CharField(max_length=40)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
