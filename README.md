# CountryLister

How to run:

1) Start ClickHouse server with command: 

   docker run -d -p 8123:8123 --name CountryListerDB --ulimit nofile=262144:262144 yandex/clickhouse-server

   (it should automatically download the ClickHouse server image, if not run following command: docker pull yandex/clickhouse-server)


2) Build the app docker image with following command:
   
   docker build -t country-lister .

3) Run the app using the newly build docker image with following command:

   docker run --network="host" -it country-lister main.py --sort-order asc

 
