FROM python:3.10-alpine AS BUILDER

COPY requirements/lock.txt /tmp/requirements
RUN pip install --no-cache-dir virtualenv               \
    && virtualenv -p python3 /opt/venv                  \
    && /opt/venv/bin/pip install                        \
        --no-cache-dir -r /tmp/requirements


FROM python:3.10-alpine

WORKDIR /app

ENV PATH /opt/venv/bin:$PATH

COPY --from=BUILDER /opt/venv /opt/venv
COPY shopping /app/shopping
COPY docker-entrypoint.sh /usr/bin/shopping

HEALTHCHECK --interval=10s --timeout=5s \
    CMD [ "/usr/bin/shopping", "healthcheck" ]

ENTRYPOINT [ "/usr/bin/shopping" ]
CMD [ "start" ]
