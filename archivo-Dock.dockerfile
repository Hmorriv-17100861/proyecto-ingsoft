FROM python:latest

ADD conexion.py /
ADD app.py /
WORKDIR /

RUN pip3 install psycopg2
RUN pip3 install flask

CMD ["python3", "app.py"]