# gastransitie project
Data handling for pilot project energy transition in Amsterdam. Currently this
project does not offer an API or webservices of any kind. We are still in an
early phase where we are determining the requirements. Maps are, for the moment,
made using QGis using a locally running PostGIS database that this software fills
with data.

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

### About current implementation
* Not all the data in this project is public. For now files reside in the
  object store and are downloaded by the scipts and uploaded to a locally
  running PostGIS instance.
* The file handling is partially done through `ogr2ogr` (GDAL) and partially
  from Python. The scripts have been set up to run in Docker containers (also
  for local development.
* Geographic data is reprojected to "Rijksdriehoek systeem"

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
