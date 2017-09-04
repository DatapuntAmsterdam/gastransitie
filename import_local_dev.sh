#!/bin/bash

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastransitie_dev -f ${DIR}/docker-compose.yml $*;
}

# trap 'dc kill ; dc rm -f -v' EXIT
echo "Setting up local dev environment."
echo "Do we have an object store password?"
echo $GASTRANSITIE_OBJECTSTORE_PASSWORD
# echo "Do we have ENVIRONMENT?"
# echo $ENVIRONMENT

dc build --pull
dc up -d database

echo "Running importer "
dc run --rm importer
dc exec -T database update-table.sh bag bag_buurt public gastransitie
# dc exec -T database update-db.sh atlas  # Download / use full BAG data dump
# dc run --rm importer /app/run_add_views.sh
dc run --rm importer bash /app/run_add_views.sh

echo "Done!"
