docker/build:
	docker build \
		-f ops/Dockerfile \
		-t ghcr.io/tmck-code/ansi-megafont:latest \
		.

docker/fonts:
	docker run --rm \
		-v ${PWD}/fonts:/app/fonts \
		ghcr.io/tmck-code/ansi-megafont:latest \
			./ops/remap.sh

docker/forge:
	docker run --rm \
		-v ${PWD}/fonts:/app/fonts \
		ghcr.io/tmck-code/ansi-megafont:latest \
			fontforge -script ./bin/forge.py \
				./fonts/remapped/ \
				./fonts/ANSICombined.ttf \
				'ANSI Combined'

all: docker/build docker/fonts docker/forge

.PHONY: docker/build docker/fonts docker/forge all