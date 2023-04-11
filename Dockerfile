FROM python:3.9.0-slim

ENV POETRY_VERSION=1.4.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /opt

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]
#здесь по сути будем накатывать миграции

EXPOSE 8000
#пробрасываем нанужу порт

#CMD ["python", "manage.py", "runserver", "-b", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
