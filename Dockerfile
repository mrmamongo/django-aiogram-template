FROM python:3.11-slim as staging

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /

RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y tini && \
    python3 -m venv venv

COPY ./requirements.txt ./manage.py ./
COPY ./template ./template/
RUN pip install -r requirements.txt && python ./manage.py collectstatic --noinput

FROM staging as dev

ENTRYPOINT ["tini", "--"]
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]

FROM staging as prod

ENTRYPOINT ["tini", "--"]
