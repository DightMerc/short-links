set -e

DOCKER="docker-compose up -d --build"

echo "Docker initialization..."
$DOCKER
echo "Done."
