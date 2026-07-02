FROM dockerhub.timeweb.cloud/library/python:3.13-slim
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./Backend /code/Backend
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini

EXPOSE 8000

CMD ["uvicorn", "Backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
