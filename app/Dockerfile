# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
FROM python:3.9

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

CMD ["./start.sh"]