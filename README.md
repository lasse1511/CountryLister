# CountryLister

How to run:

1) Start ClickHouse server with command: 
   docker run -d --name CountryListerDB --ulimit nofile=262144:262144 yandex/clickhouse-server
   (it should automatically download the ClickHouse server image, if not run following command: docker pull yandex/clickhouse-server)
   
2) 
