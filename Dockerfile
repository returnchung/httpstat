FROM python:3.8.2-alpine3.11

RUN apk add --no-cache jq bind-tools

WORKDIR /root

COPY httpstat requirements.txt index.py entrypoint.sh ./

RUN pip install -U pip \
    && pip install -r requirements.txt

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

ENTRYPOINT ["/root/entrypoint.sh"]
