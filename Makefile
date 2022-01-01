GIT_COMMIT = $(shell git rev-parse HEAD)

docker_build:
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t ghcr.io/enghabu/wireless-fencing:$(GIT_COMMIT) .

docker_push: docker_build
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t ghcr.io/enghabu/wireless-fencing:$(GIT_COMMIT) --push .

docker_run: docker_build
	docker run -p 8080:8080 ghcr.io/enghabu/wireless-fencing:$(GIT_COMMIT)

start-server:
	cd webserver && python -m uvicorn main:app --reload