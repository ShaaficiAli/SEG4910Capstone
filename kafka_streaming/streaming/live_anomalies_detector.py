import json
import os
from joblib import load
import logging
from multiprocessing import Process
import regex as re
from sklearn import *
import numpy as np

from utils import create_producer, create_consumer
from settings import TRANSACTIONS_TOPIC, TRANSACTIONS_CONSUMER_GROUP, ANOMALIES_TOPIC, NUM_PARTITIONS

model_path = os.path.abspath('../model/log_regression_dns.joblib')

def format(data):

    #removing []
    data = data[1:-1]
    data = data.replace("'","")

    array = re.findall(r'\d+(?:\.\d+)?', data)

    array[0] = int(array[0])
    array[1] = int(array[1])
    array[2] = int(array[2])
    array[3] = int(array[3])
    array[4] = int(array[4])
    array[5] = float(array[5])
    array[6] = int(array[6])
    array[7] = int(array[7])
    array[8] = float(array[8])
    array[9] = int(array[9])
    array[10] = int(array[10])

    array.pop(0)
    x = [array]
    return x

def detect():
    consumer = create_consumer(topic=TRANSACTIONS_TOPIC, group_id=TRANSACTIONS_CONSUMER_GROUP)

    producer = create_producer()

    model = load(model_path)

    while True:
        message = consumer.poll(timeout=5)
        if message is None:
            print("no message")
            continue
        if message.error():
            logging.error("Consumer error: {}".format(message.error()))
            print("Consumer error")
            continue

        # Message that came from producer
        record = json.loads(message.value().decode('utf-8'))
        #DROP WEBSITE
        data = record["data"][0]

        data2 = list(data.values())
        data2 = data2[:-1]

        print(data2)
        prediction = model.predict([data2])

        data_string = ' '.join(map(str, data2))

        record2 = str(record["id"]) + " " + str(prediction[0]) + " " + data_string + " " + str(record["Website"])
        
        new_record = json.dumps(record2).encode("utf-8")

        print(prediction)

        producer.produce(topic=ANOMALIES_TOPIC,
                             value=new_record)
        producer.flush()

        # consumer.commit() # Uncomment to process all messages, not just new ones

    consumer.close()


if __name__ ==  '__main__':
# One consumer per partition
    for _ in range(NUM_PARTITIONS):
        p = Process(target=detect)
        p.start()
