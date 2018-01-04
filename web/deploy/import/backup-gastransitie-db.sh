#!/usr/bin/env bash

set -x
set -e
set -u

echo 0.0.0.0:5432:gastransitie:gastransitie:insecure > ~/.pgpass
chmod 600 ~/.pgpass

pg_dump --clean \
	-Fc \
	-t gas_afwc2017 \
	-t gas_cbs_buurt_2017_raw \
	-t django_* \
	-U gastransitie \
	-h 0.0.0.0 \
	-p 5432 \
	gastransitie > /tmp/backups/database.dump
