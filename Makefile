.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8

include .env

all: docker

run:
	uvicorn dht22_fastapi.dht22_fastapi:app --reload

docker: docker-build docker-push

docker-build:
	docker build -t $(REMOTE_REPO_URL):latest . --build-arg USER=${USER} --build-arg PASS=${PASS}

docker-push:
	docker push $(REMOTE_REPO_URL):latest
