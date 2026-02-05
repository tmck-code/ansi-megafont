docker/build:
	docker build -f ops/Dockerfile -t ghcr.io/tmck-code/ansi-megafont:latest .

docker/fonts:
	docker run --rm \
		-v ${PWD}/fonts/remapped:/app/fonts/remapped \
		ghcr.io/tmck-code/ansi-megafont:latest \
			./ops/remap.sh

docker/forge:
	docker run --rm \
		-v ${PWD}/fonts/remapped:/app/fonts/remapped \
		-v ${PWD}/dist:/app/dist \
		ghcr.io/tmck-code/ansi-megafont:latest \
			bash -c "fontforge -script ./bin/forge.py ./fonts/remapped/ ANSICombined"

all: docker/build docker/fonts docker/forge

.PHONY: docker/build docker/fonts docker/forge all