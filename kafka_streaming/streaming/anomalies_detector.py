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
        data = record["data"]
        
        #formatted = [[int(data[0]["Length"])],[int(data[0]["Subdomain length"])],[int(data[0]["Uppercase count"])],
        #    [int(data[0]["Lowercase count"])],[int(data[0]["Numeric count"])],[float(data[0]["Entropy"])],
        #    [int(data[0]["Length"])],[int(data[0]["Special Char Count"])],[int(data[0]["Max label length"])],
        #    [int(data[0]["Average label length"])],[int(data[0]["Number of Labels"])],[int(data[0]["Number of Labels"])],
        #    [int(data[0]["Length of domain"])]]

        prediction = model.predict(format(data))

        """
        # If an anomaly comes in, send it to anomalies topic
        if prediction[0] == -1:
            #replace clf with model
            score = clf.score_samples(data)
            record["score"] = np.round(score, 3).tolist()

            _id = str(record["id"])
            record = json.dumps(record).encode("utf-8")

            producer.produce(topic=ANOMALIES_TOPIC,
                             value=record)
            producer.flush()

            #record = {"id": _id, "data": df_json_data, "Website": str(df_website.iloc[0]), "Timestamp": current_time}
        """
        #prediction = 1
        new_record = {"id": record["id"], "prediction": str(prediction), "data": record["data"], "website": record["Website"], "timestamp": record["Timestamp"]}
        new_record = json.dumps(record).encode("utf-8")

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
