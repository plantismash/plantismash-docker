source .envs

# echo "Running job count update script"
# python3 update_job_count.py --url $STATUS_URL --settings $SETTINGS_FILE

echo "Rebuilding docker images. this may take some time"
docker build --tag plantismash-web:latest web --no-cache
# docker build --tag plantismash-backend:latest backend --no-cache

echo "Stopping docker services"
docker-compose stop plantismash-web

echo "Removing old containers"
docker-compose rm plantismash-web

echo echo "Recreating containers"
docker-compose create plantismash-web

echo "restarting containers"
docker-compose start plantismash-web
