FROM nvidia/cuda:12.4.0-base-ubuntu22.04 AS base

ENV PYTHON_VERSION=3.10

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y update \
    && apt-get -y install --no-install-recommends \
    python${PYTHON_VERSION} \
    python3-pip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s -f /usr/bin/python${PYTHON_VERSION} /usr/bin/python3 && \
    ln -s -f /usr/bin/python${PYTHON_VERSION} /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

WORKDIR /app

RUN apt-get update && \
	apt-get install --no-install-recommends -y apt-transport-https ca-certificates ffmpeg  \
	&& apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY ./requirements.txt .

RUN pip install --upgrade pip --no-cache-dir && \
	pip install -r requirements.txt --no-warn-script-location --no-cache-dir --compile && \
    pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu122/torch_stable.html

FROM base AS base_code
WORKDIR /code

COPY . .

FROM base_code AS test_runner
WORKDIR /code
RUN pip install --upgrade pip --no-cache-dir \
    && pip install pytest scipy --no-cache-dir \
    && rm -rf /var/lib/apt/lists/*

RUN pytest

CMD ["python3", "/code/whisper_service/__init__.py"]
VOLUME /root/.cache/whisper