# Energie transitie project
Data handling for pilot project energy transition in Amsterdam.

### Context:
* A number of stakeholders have gotten together to select a number of
  neighborhoods in Amsterdam that will be part of a pilot project to
  remove the gas-mains connections to the housing / buildings and replace
  it with electrics and district heating.
* Each of these stakeholders has some data they are willing to share with
  the other stakeholders. While they have data, they have no way of
  visualizing the data.
* Goal of the visualizations and reporting are to:
  1. Compare and contrast the different neighborhoods in Amsterdam to select
     a few that are candidates for the pilot project.
  2. For candidate pilot neighborhoods drill down in the data to see whether
     they are really good candidates.

## About the new implementation (which is work-in-progress)
* The new version will provide a Django application (under `web/`).
* This web app provides detail pages for each Amsterdam neighborhood based on
  quick scan documents currently used internally.
* Furthermore some city wide overview maps will also be provided for comparison.
* The file handling is partially done through `ogr2ogr` (GDAL) and partially
  from Python. The scripts have been set up to run in Docker containers (also
  for local development.
* Geodata is reprojected to EPSG:4326 (WGS 84) before storage.
* A Django web application is being developed to show factsheets per
  neighborhood.

### Runnning locally
All this assumes you work for the Energie transitie / Datapunt team and have
access to the relevant credentials.

* Check out the repository.
* Set the `GASTRANSITIE_OBJECTSTORE_PASSWORD` environment variable.
* Run the following commands in the repository root. Note: <username> is the
  user associated with the SSH key that Datapunt registered for you.

```
    export GASTRANSITIE_OBJECTSTORE_PASSWORD=<password>
    docker-compose pull
    docker-compose up -d database
    docker-compose run --rm web python manage.py migrate
    docker-compose run --rm web python manage.py download_data
    docker-compose run --rm web python manage.py run_import
    docker-compose exec database update-table.sh bag bag_buurt public gastransitie <username>
    docker-compose run --rm web python manage.py fix_tables
    docker-compose up web
```

### Data sources
Currently all these are backed-up on the object store.
* Planned renovations of social housing - non-public, source AFWC
* Alliander gas mains in two categories (orange, and gree) - non-public, source
  Alliander
* District heating network - source Nuon by way of maps.amsterdam.nl
* Large projects "Meerjarig Investerings Plan 2016" - source Stadsregie by way
  maps.amsterdam.nl
* Owners of social housing - source maps.amsterdam.nl
* "Energie labels" (Dutch system that labels houses with their energy usage) -
  source maps.amsterdam.nl
* CBS neighborhoods / labels - source CBS website
* Amsterdam neighborhoods / labels - source BAG webservice maintained by Amsterdam
* "Eigendomskaart" (classifies owners of real estate in Amsterdam) - non-public,
  source OIS
* "Functiekaart" (classifies usage of real estate in Amsterdam other than
  housing) - non-public, source OIS


### Browsing the API with Swagger-UI

Make sure the service is running locally (see instructions above), then run:

```
$ docker-compose up -d swaggerui
$ open http://localhost:8686/swagger-ui/?url=http://localhost:8000/gastransitie/dash/openapi.yml#/default/get_gastransitie_api_afwc_
```