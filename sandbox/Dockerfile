FROM python:3.12-slim

RUN useradd --uid 65532 --no-create-home --shell /usr/sbin/nologin sandbox-user

USER 65532:65532
WORKDIR /app

COPY --chown=65532:65532 scripts/parse_llgx.py /app/parse_llgx.py

ENTRYPOINT ["python", "/app/parse_llgx.py"]
