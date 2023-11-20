FROM --platform=linux/amd64 python:3.8.13-slim-buster

RUN apt-get update -y && apt-get install -y jq bind9

WORKDIR /root

COPY httpstat httpstat
COPY requirements.txt index.py entrypoint.sh ./

RUN chmod +x entrypoint.sh

RUN pip install -U pip \
    && pip install -r requirements.txt

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

ENTRYPOINT ["/root/entrypoint.sh"]
