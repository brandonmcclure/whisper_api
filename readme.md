# whisper_service

A quick and basic Open AI Whisper written in python using a gradio UI and API. 

I wrote this to offload STT functionality from old or CPU only computers onto a more beefy server. This has been serving my needs well and is pretty simple so I want to share. I am open to pull requests or issues, although my primary goal for this service is to keep it simple.

## To Build

you need `docker`, `gnu make`, `powershell core` to run the makefile. Read the makefile to run the docker build command directly. 

Run `make build`
## To Run

`docker run -d -p 7861:7861 -v /mnt/TANK/apps/ai/whisper/cache:/root/.cache/whisper bmcclure89/whisper_api:main`

Mounting the volume is optional, but pre