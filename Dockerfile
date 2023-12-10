FROM nvidia/cuda:12.2.0-base-ubuntu22.04

ENV PYTHON_VERSION=3.10

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --no-install-recommends \
    python${PYTHON_VERSION} \
    python3-pip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s -f /usr/bin/python${PYTHON_VERSION} /usr/bin/python3 && \
    ln -s -f /usr/bin/python${PYTHON_VERSION} /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

WORKDIR /app

RUN apt-get update && \
	apt-get install -y apt-transport-https ca-certificates ffmpeg --no-install-recommends \
	&& apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY ./requirements.txt .

RUN pip install --upgrade pip --no-cache-dir && \
	pip install -r requirements.txt --no-warn-script-location --no-cache-dir --compile

WORKDIR /code

COPY . .

CMD ["python3", "/code/main.py"]