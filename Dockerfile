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

COPY ./requirements.in ./manage.py ./
RUN pip install --no-input pip-tools && \
    pip-compile -o requirements.txt ./requirements.in && \
    pip uninstall --no-input -y pip-tools && \
    pip install -r requirements.txt

COPY ./template ./template/
RUN python ./manage.py collectstatic --noinput

FROM staging as dev

ENTRYPOINT ["tini", "--"]
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]

FROM staging as prod

ENTRYPOINT ["tini", "--"]
