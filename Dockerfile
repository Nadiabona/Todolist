FROM python:3.9.0-slim



WORKDIR /opt

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]
#здесь по сути будем накатывать миграции

EXPOSE 8000
#пробрасываем нанужу порт

#CMD ["python", "manage.py", "runserver", "-b", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
