#!/bin/sh

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastransitie -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc rm -f' EXIT

# For database backups:
rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

echo "For debugging list volumes"
dc down	-v
dc rm -f
dc pull

docker volume ls

echo "Building images"
dc build

echo "Bringing up and waiting for database"
dc up -d database
dc run importer /deploy/docker-wait.sh

echo "Downloading raw datafiles from object store"
dc run --rm importer ls /data
dc run --rm importer python manage.py download_data
dc run --rm importer ls /data

dc exec -T database update-table.sh bag bag_buurt public gastransitie
dc exec -T database update-db.sh bag

echo "Importing data into database"

dc run --rm importer python manage.py migrate
# import alle objectstore bronnen
dc run --rm importer python manage.py run_import

dc run --rm importer python manage.py run_import --indexgebied
dc run --rm importer python manage.py run_import --handelsregister
dc run --rm importer python manage.py run_import --sbicodes
dc run --rm importer python manage.py run_import --hrrapport
dc run --rm importer python manage.py run_import --brkbag

echo "Running backups"
dc exec -T database backup-db.sh gastransitie

echo "Remove containers and volumes."
dc down -v
dc rm -f

echo "Done"
