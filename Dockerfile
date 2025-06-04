FROM python:3-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --upgrade pip wheel setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

# Default port (can be configured in config.json)
EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "ferelight"]
