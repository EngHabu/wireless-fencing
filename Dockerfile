FROM python:3.9
WORKDIR /code/webserver
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./webserver /code/webserver

CMD ["python", "main.py"]
