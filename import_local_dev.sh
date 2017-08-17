#!/bin/bash

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastransitie_dev -f ${DIR}/docker-compose.yml $*;
}

dc pull

# trap 'dc kill ; dc rm -f -v' EXIT
echo "Setting up local dev environment."
echo "Do we have an object store password?"
echo $GASTRANSITIE_OBJECTSTORE_PASSWORD
echo "Do we have ENVIRONMENT?"
echo $ENVIRONMENT

# rm -rf ${DIR}/backups
# mkdir -p ${DIR}/backups

dc build --pull

dc up -d database

# load latest bag into database
echo "Load latest verblijfsobjecten en nummeraanduidingen in gastransitie database"

dc run --rm importer /app/docker-wait.sh
dc exec -T database update-table.sh bag bag_buurt public gastransitie
# dc exec -T database update-db.sh atlas  # Download / use full BAG data dump

echo "Running importer "
dc run --rm importer

echo "Done!"
