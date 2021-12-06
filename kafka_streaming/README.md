# kafkaml-dns detection

Project for real time anomaly detection using kafka and python

It's assumed that zookeeper and kafka are running in the localhost, it follows this process:

First RUN 

bin/zookeeper-server-start.sh config/zookeeper.properties

Then 

bin/kafka-server-start.sh config/server.properties

The create first topic 

./bin/kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 

./bin/kafka-topics.sh --create --topic anomalies --bootstrap-server localhost:9092 --create --partitions 3 --replication-factor 1

Check to see if topics were created 

./bin/kafka-topics.sh --bootstrap-server localhost:9092 --list 

To delete topics 

./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic anomalies 
./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic transactions 


Make sure elasticsearch and logstash are the EXACT same version 

Debug elasticsearch

jps | grep Elasticsearch

kill -SIGTERM "elastic search PID"

Logstash 

logstash-7.13.0/bin/logstash -f kafka_input.conf

If you dont see indexes in kibana go to stack management refresh fields