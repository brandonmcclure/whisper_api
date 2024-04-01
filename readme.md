# whisper_service

[![Docker Stars](https://img.shields.io/docker/stars/bmcclure89/whisper_service.svg?style=flat-square)](https://hub.docker.com/r/bmcclure89/whisper_service/) [![Docker Pulls](https://img.shields.io/docker/pulls/bmcclure89/whisper_service.svg?style=flat-square)](https://hub.docker.com/r/bmcclure89/whisper_service/)

A quick and basic Open AI Whisper written in python using a gradio UI and API. 

I wrote this to offload STT functionality from old or CPU only computers onto a more beefy server. This has been serving my needs well and is pretty simple so I want to share. I am open to pull requests or issues, although my primary goal for this service is to keep it simple.

## To Build

you need `docker`, `gnu make` to run the makefile. Read the makefile to run the docker build command directly. 

Run `make` to build the docker image. It will run the python tests as part of the docker build. 

## To Run

I recommend to run with a GPU, although it does work [cpu only](#cpu-only). Getting your docker host to work with gpus is outside the scope, but checkout [docker documentation](https://docs.docker.com/config/containers/resource_constraints/#gpu) if you are interested in more.

```
docker run -d --gpus=all -p 127.0.0.1:7861:7861 -v whisper_cache:/root/.cache/whisper bmcclure89/whisper_service:main
```

`whisper_cache` is where the whisper models will be stored the first time they are needed. See [openai documentation](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages) of the different models you can use.

### Cpu Only

This is pretty slow, but you can get it to run by passing the `--cpu` flag to the python module. To run a docker container without gpu support use:

```
docker run -d -p 127.0.0.1:7861:7861 -v whisper_cache:/root/.cache/whisper bmcclure89/whisper_service:main python3 /code/whisper_service/__init__.py --cpu
```