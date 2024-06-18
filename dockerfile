FROM python:3.10-alpine
WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8010:8010

VOLUME data

ENV DB_LOCATION=/data/contacts.db
ENV ENVIRONMENT=production

CMD ["python", "main.py"]