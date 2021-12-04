# kafkaml-dns-detection

It's assumed that zookeeper and kafka are running in the localhost, it follows this process:

# Demo

Producer and anomaly detection running at the same time

# Kafka set up

First RUN 

bin/zookeeper-server-start.sh config/zookeeper.properties

Then 

bin/kafka-server-start.sh config/server.properties

The create first topic 

kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 

kafka-topics.sh --create --topic anomalies --bootstrap-server localhost:9092 --create --partitions 3 --replication-factor 1

Check to see if topics were created 

./bin/kafka-topics.sh --bootstrap-server localhost:9092 --list 

To delete topics 

./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic anomalies 
./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic transactions 



# Usage:

* First train the anomaly detection model, run the file:

```bash
model/train.py
```

* Create the required topics

```bash
kafka-topics.sh --zookeeper localhost:2181 --topic transactions --create --partitions 3 --replication-factor 1
kafka-topics.sh --zookeeper localhost:2181 --topic anomalies --create --partitions 3 --replication-factor 1
```

* Check the topics are created

```bash
kafka-topics.sh --zookeeper localhost:2181 --list
```

* Check file **settings.py** and edit the variables if needed

* Start the producer, run the file

```bash
streaming/producer.py
```

* Start the anomalies detector, run the file

```bash
streaming/anomalies_detector.py
```

* start connection to second broker

```bash
streaming/bot_alerts.py
```
