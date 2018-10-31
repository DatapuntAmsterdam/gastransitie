#!/bin/sh

set -e
set -u
set -x

POSTGRES_USER=gastransitie

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastransitie${ENVIRONMENT} -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc down ; dc rm -f' EXIT

# For database backups:
rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

dc down	-v
dc rm -f
dc pull

echo "Building images"
dc build

echo "Bringing up and waiting for database"
dc up -d database
dc run importer /deploy/docker-wait.sh

dc exec -T database createuser -U $POSTGRES_USER postgres || echo "Could not create postgres, continuing"
echo "Downloading raw datafiles from object store"
# dc run --rm importer ls /data
dc run --rm importer python manage.py download_data
# dc run --rm importer ls /data
#
dc exec -T database update-table.sh bag bag_buurt public gastransitie
dc exec -T database update-db.sh bag

echo "Importing data into database"

dc run --rm importer python manage.py migrate
# import alle objectstore bronnen
dc run --rm importer python manage.py run_import

dc run --rm importer python manage.py run_import --indexgebied
dc run --rm importer python manage.py run_import --brkbag
dc run --rm importer python manage.py run_import --handelsregister
dc run --rm importer python manage.py run_import --sbicodes
dc run --rm importer python manage.py run_import --hrrapport

echo "Running backups"
dc exec -T database backup-db.sh gastransitie

echo "Remove containers and volumes."
dc down -v
dc rm -f

echo "Done"
