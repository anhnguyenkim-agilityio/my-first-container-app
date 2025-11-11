#!/bin/bash

set -e
cmd="$@"

# Runs database migration if DATABASE_MIGRATE flag is set
echo "Db Migrate: $DATABASE_MIGRATE"
# if [[ "$DATABASE_MIGRATE" == "true" ]]; then
./bin/dj-migrate.sh
# fi

# Loads test data if GENERATE_SAMPLE_DATA is turned on
echo "Generate Sample Data: $GENERATE_SAMPLE_DATA"
if [[ "$GENERATE_SAMPLE_DATA" == "true" ]]; then
    ./bin/dj-initdata.sh
fi

echo "Collect statics: $COLLECT_STATICS"
# if [[ "$COLLECT_STATICS" == "true" ]]; then
./bin/dj-collectstatics.sh
# fi

echo "All ready"

exec $cmd
