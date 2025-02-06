# syntax=docker/dockerfile:1

FROM ubuntu
RUN apt-get -y update
RUN apt-get -y install python3 python-is-python3 python3-pip python3-venv

COPY dht22_fastapi/dht22_fastapi.py /app/app.py
COPY requirements.txt /app/
RUN mkdir /app/static
COPY templates/test-sse-deployed.html /app/templates/test-sse-deployed.html
WORKDIR /app/

RUN python -m venv venv
RUN . venv/bin/activate && pip config --user set global.extra-index https://gitea.app.brisecom.net/api/packages/fjavier/pypi
RUN . venv/bin/activate && pip config --user set global.extra-index-url https://gitea.app.brisecom.net/api/packages/fjavier/pypi/simple
RUN . venv/bin/activate && pip config --user set global.trusted-host gitea.app.brisecom.net

RUN . venv/bin/activate && pip install --upgrade pip
RUN . venv/bin/activate && pip install -r requirements.txt

CMD venv/bin/python uvicorn app:app --host 0.0.0.0 --port 8000
EXPOSE 8000
