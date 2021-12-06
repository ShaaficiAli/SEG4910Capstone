# SEG4910Capstone
Capstone project
This code is written entirely in Python3

Python libraries to install:
Numpy
Pandas
Pyspark
Scapy
Kafka-python

Any missing dependancy should be easily installed with pip3 i.e. "pip3 install dependancy"

To run the model code in this project PySpark must be installed correctly on your machine. Following the instructions here can be helpful: https://www.datacamp.com/community/tutorials/installation-of-pyspark?fbclid=IwAR34jVsMn_GuscJTadoQBakhfuQwTTfIYzovzNO-_J5lCWhsXYdw3I0WFhE

**To run the full stack, i.e. Kafka, the model, elasticsearch, and kibana, the ELK stack must be correctly configured
**
It's assumed that zookeeper and kafka are running in the localhost, it follows this process (after downloading Kafka and opening a terminal in the directory):

**First RUN (In one terminal, leave it running):**

bin/zookeeper-server-start.sh config/zookeeper.properties

**Then (In a second terminal, leave it running):**

bin/kafka-server-start.sh config/server.properties

**Then create both topics (In a third terminal, run these one at a time):**

./bin/kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3

./bin/kafka-topics.sh --create --topic anomalies --bootstrap-server localhost:9092 --create --partitions 3 --replication-factor 1

**Check to see if topics were created**

./bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

**To delete topics**

./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic anomalies ./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic transactions

**Next download elasticsearch and logstash - make sure elasticsearch and logstash are the EXACT same version**

Debug elasticsearch

jps | grep Elasticsearch

kill -SIGTERM "elastic search PID"

**Logstash**

logstash-7.13.0/bin/logstash -f kafka_input.conf

Then run kibana - If you dont see indexes in kibana go to stack management refresh fields

Structure of repository:
Inside SEG4910Capstone folder is where our code for running our models is.
Kafka_streaming has the code for running the model with kafka and kibana dashboard


**Data Scripts:**

A folder that contains datasets used and generated as well as the scripts that were used to generate them

**Docs:**

A folder for documents that will be used in the next semester

**Models:**

A folder containing all the models that are used as well as our 
model utils library that helps model/model data creation and evaluation

**Notebooks:**

A folder for jupyter notebooks that will be used next semester

**References:**

A folder that will contain references used next semester

**Reports:**

A folder containing reports that will be used next semester

**Relevant folders for this semester are:**

Data scripts and models

To run a model go to: 
SEG4910Capstone > models  

Then open file location in command line and run:
"python3 modelname.py"

