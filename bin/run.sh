#! /bin/sh

docker build -t bridge . &&
docker run -e DRY_RUN=1 --rm -t bridge python cli.py $1
