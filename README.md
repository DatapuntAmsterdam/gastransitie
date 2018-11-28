# Creates neighborhood information dashboard related to energy.

      
            +-------------------------------+
            | Buurten ~480                  |
            |                               |
            +--------------+----------------+
                           |
                           |
                           +<------+ Renovaties
           Meerjarig       |
           investerings    |
           Plan mip------ >+
                           |
                           +<-------+ Coorporatie bezit
                           |
                           |
          Gasverbruik      +<-------+ Eigenaren
               +--------->>+
                           |
          Warmte Koude     |          Handelsregister
                   +------>+         +Acitviteiten
          Energie labels   |         |
                  +------->+         |
                           |         |
                           <---------+
                           |
          +----------------+---------------+
          |   Rapport per buurt.           |
          |                                |
          |                                |
          |                                |
          +--------------------------------+




# Energy Transition Project / Energie transitie project

Data dashboard providing information about gas / energy information
of the city of Amsterdam. All stakeholders provide information relevant
for an efficient transition away from gas energy. This repository contains
both a backend and a frontend path of the dashboard web application.

### Context
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


### Run the application locally or work on its frontend
All this assumes you work for the Energie transitie / Datapunt team and have
access to the relevant credentials. In particular your SSH key must be known
by Amsterdam Datapunt to allow downloads of database backups.

* Check out this repository, move to the repository root.
* Run the following commands to download a database backup and start the
  backend services:
  ```
  docker-compose pull
  docker-compose build
  docker-compose up -d database
  docker-compose exec database update-db.sh gastransitie <username>
  docker-compose up web swaggerui
  ```
* To start the frontend in development mode run the following commands
  (starting at the repository root).
  ```
  cd frontend
  rm -rf node_modules
  npm install
  npm run dev
  ```

You can now access the application at http://localhost:8000.

### Working on the Backend (in locally running Docker containers)
You can follow the instructions above if you are not touching the import
process. However, if you need to work on the import process or need to run
that process locally follow the instructions below (assuming you have the
relevant credentials and your SSH key is known).

* Access the RATTIC password for the energietransitie project and set the
  the `GASTRANSITIE_OBJECTSTORE_PASSWORD` environment variable:
  ```
  export GASTRANSITIE_OBJECTSTORE_PASSWORD=<password>
  ```
* Check out this repository, move to the repository root.
* Run the following commands to download a database backup and start the
  backend services:
  ```
  docker-compose pull
  docker-compose build
  docker-compose up -d database
  ```
* Wait for the database to start up, then run
  ```
  docker-compose run --rm web python manage.py download_data
  docker-compose exec -T database update-table.sh bag bag_buurt public gastransitie <username>
  docker-compose exec -T database update-db.sh bag <username>
  ```
  Note that downloading these database backups and restoring them is time
  consuming (but the BAG database is needed to generate some of the
  neighborhood summaries).
* Then run the Django management commands for imports:
  ```
  docker-compose run --rm web python manage.py run_import

  docker-compose run --rm web python manage.py run_import --indexgebied
  docker-compose run --rm web python manage.py run_import --brkbag
  docker-compose run --rm web python manage.py run_import --handelsregister
  docker-compose run --rm web python manage.py run_import --sbicodes
  docker-compose run --rm web python manage.py run_import --hrrapport
  ```
* Now start the services:
  ```
  docker-compose up web swaggerui
  ```

The source directories for the Django web application use a bind mount into
the running Docker container. Furthermore the Django development server is used
so there is no need to manually reload the application on a source update.

### Creating the map "energieverbruik" layer
A normal full import run of the gastransitie project will also create the
energie verbruik map layer (as part of the Alliander import step). The map
layer is constructed using open Alliander energy usage data and the BAG
database that contains the "panden" (~buildings) and their postal codes.

In the commands below replace `<password>` with the actual object store
password and `<username>` with your username (assuming you are authorized to
access the data).

```
export GASTRANSITIE_OBJECTSTORE_PASSWORD=<password>
docker-compose pull
docker-compose build
docker-compose up -d database
docker-compose exec -T database update-db.sh bag <username>
docker-compose run --rm web python manage.py download_data
docker-compose --rm web python manage.py migrate
docker-compose run --rm web python manage.py run_import --alliander
```

(Note: this is only relevant if you did not import the full dataset as
described in the previous section.)

### Running the tests
You can run the tests for the `web` container that does both the imports
and serve the API, using the following command (after building the containers).

```
docker-compose run web python manage.py test --nomigrations
```


### Notes on the implementation
* The file handling is partially done through `ogr2ogr` (GDAL) and partially
  from Python. The scripts have been set up to run in Docker containers (also
  for local development.
* Geodata is reprojected to the EPSG:4326 (WGS 84) coordinate system before
  storage and served that way as well.


### Data sources
Data received through are partners and stored on the object store:
* Planned renovations of social housing - non-public, source AFWC
* Alliander gas mains in two categories (orange, and gree) - non-public, source
  Alliander
* District heating network - source Nuon by way of maps.amsterdam.nl
* Large projects "Meerjarig Investerings Plan 2016" - source Stadsregie by way
  maps.amsterdam.nl
* "Energie labels" (Dutch system that labels houses with their energy usage) -
  source maps.amsterdam.nl

Data accessed through the Amsterdam Datapunt infrastructure:
* BAG (Basisregistratie adressen en gebouwen)
* BRK


### Browsing the API with Swagger-UI

Make sure the service is running locally (see instructions above), then run:

```
$ docker-compose up -d swaggerui
$ open http://localhost:8686/swagger-ui/?url=http://localhost:8000/gastransitie/dash/openapi.yml#/default/get_gastransitie_api_afwc_
```

Note that the Swagger docs are a work-in-progress still.
