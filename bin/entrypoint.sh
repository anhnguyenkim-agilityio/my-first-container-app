set -e
cmd="$@"

./bin/dj-migrate.sh
./bin/dj-collectstatics.sh

echo "All ready"

exec $cmd
