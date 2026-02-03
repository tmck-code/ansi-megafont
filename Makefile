docker/build:
	docker build -f ops/Dockerfile -t ghcr.io/tmck-code/ansi-megafont:latest .

docker/fonts:
	docker run --rm \
		-v ${PWD}/patched:/app/patched \
		ghcr.io/tmck-code/ansi-megafont:latest \
			./ops/remap.sh

docker/forge:
	docker run --rm \
		-v ${PWD}/patched:/app/patched \
		-v ${PWD}/dist:/app/dist \
		ghcr.io/tmck-code/ansi-megafont:latest \
			bash -c "fontforge -script ./bin/forge.py ./patched/ TopazPlusPlus 2> /dev/null"

all: docker/build docker/fonts docker/forge

.PHONY: docker/build docker/fonts docker/forge all