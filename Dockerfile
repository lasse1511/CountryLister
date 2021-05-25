FROM python:3
WORKDIR /usr/src/app
COPY . .
CMD ["main.py"]
ENTRYPOINT ["python3"]
RUN apt-get update
RUN pip install pandas
RUN pip install clickhouse-driver