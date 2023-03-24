#! /bin/sh

docker build --build-arg ENVIRONMENT=test -t bridge_test . &&
docker run --rm -t bridge_test pytest -s --pylint -vv
