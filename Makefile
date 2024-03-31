.PHONY: all clean test lint
all: build

REGISTRY_NAME :=
REPOSITORY_NAME := bmcclure89/
IMAGE_NAME := whisper_service
TAG := :latest

# Run Options
RUN_PORTS := -p 7861:7861

getcommitid: 
	$(eval COMMITID = $(shell git log -1 --pretty=format:"%H"))
getbranchname:
	$(eval BRANCH_NAME = $(shell echo "$$(git branch --show-current)" | sed 's/\//./g'))
get_file_safe_image_name:
	$(eval IMAGE_TAR_FILE_NAME = $(shell echo "$(IMAGE_NAME)" | sed 's/\//./g').tar)

build: getcommitid getbranchname
	docker build -t $(REGISTRY_NAME)$(REPOSITORY_NAME)$(IMAGE_NAME)$(TAG) -t $(REGISTRY_NAME)$(REPOSITORY_NAME)$(IMAGE_NAME):$(BRANCH_NAME) -t $(REGISTRY_NAME)$(REPOSITORY_NAME)$(IMAGE_NAME):$(BRANCH_NAME)_$(COMMITID) .

run: build
	docker run --gpus=all -it $(RUN_PORTS) -v whisper_cache:/root/.cache/whisper $(REGISTRY_NAME)$(REPOSITORY_NAME)$(IMAGE_NAME)$(TAG)
package: get_file_safe_image_name
	docker save $(REGISTRY_NAME)$(REPOSITORY_NAME)$(IMAGE_NAME)$(TAG) -o $(IMAGE_TAR_FILE_NAME)

size:
	docker inspect -f "{{ .Size }}" $(REGISTRY_NAME)$(REPOSITORY_NAME)$(IMAGE_NAME)$(TAG)
	docker history $(REGISTRY_NAME)$(REPOSITORY_NAME)$(IMAGE_NAME)$(TAG)

publish:
	docker login; docker push $(REGISTRY_NAME)$(REPOSITORY_NAME)$(IMAGE_NAME)$(TAG); docker logout
lint: lint_makefile
lint_makefile:
	docker run -v $${PWD}:/tmp/lint -e ENABLE_LINTERS=MAKEFILE_CHECKMAKE oxsecurity/megalinter-ci_light:v6.10.0

venv_create:
	python -m venv ".venv"

venv_activate:
	source "./.venv/bin/activate"

venv_deactivate:
	. "./.venv/bin/deactivate"

install_reqs: 
	pip install -r 'requirements.txt'

precommit_install:
	pre-commit install
precommit_checkall: precommit_install
	pre-commit run --all-files
