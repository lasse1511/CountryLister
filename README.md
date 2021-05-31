# CountryLister

How to run:

1) Start ClickHouse server with command: 

   docker run -d -p 9000:9000 -p 8123:8123 --name CountryListerDB --ulimit nofile=262144:262144 yandex/clickhouse-server

   (it should automatically download the ClickHouse server image, if not run following command: docker pull yandex/clickhouse-server)


2) CD to app directory (where main.py is)


3) Build the app docker image with following command:
   
   docker build -t country-lister .


4) Run the app using the newly build docker image with following command:

   docker run --network="host" -it country-lister main.py

 
