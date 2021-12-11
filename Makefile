GIT_COMMIT = $(shell git rev-parse HEAD)

docker_build:
	docker build -t ghcr.io/enghabu/wireless-fencing:$(GIT_COMMIT) .

docker_push: docker_build
	docker push ghcr.io/enghabu/wireless-fencing:$(GIT_COMMIT)

docker_run: docker_build
	docker run -d -p 8080:8080 ghcr.io/enghabu/wireless-fencing:$(GIT_COMMIT)
