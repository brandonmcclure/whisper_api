FROM python:3.12
RUN apt-get update && \
	apt-get install -y apt-transport-https ca-certificates --no-install-recommends \
	&& apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY ./requirements.txt .

RUN pip install --upgrade pip --no-cache-dir && \
	pip install -r requirements.txt --no-warn-script-location --no-cache-dir --compile

WORKDIR /code

COPY . .

CMD ["python3", "/code/main.py"]