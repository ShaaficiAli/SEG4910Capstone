import json
import random
import time
from datetime import datetime
import pandas as pd

import numpy as np

from settings import TRANSACTIONS_TOPIC, DELAY, OUTLIERS_GENERATION_PROBABILITY
from utils import create_producer

df = pd.read_csv('TestDataset.csv',index_col=[0])

_id = 0
producer = create_producer()

if producer is not None:
    for i in range (0,100000):
        time.sleep(DELAY)
        df_new = df.sample()
        df_website = df_new["Website"].iloc[0]

        #Need to drop website before training
        #df=df.drop('Website',1)

        new_df = df_new.drop(['Website', 'Label'], axis = 1)

        df_json_data = new_df.to_json(orient='records')
        print(df_json_data)

        current_time = datetime.utcnow().isoformat()
        record = {"id": _id, "data": df_json_data, "Website": df_website, "Timestamp": current_time}
        print(record)

        record = json.dumps(record).encode("utf-8")

        
        producer.produce(topic=TRANSACTIONS_TOPIC,
                             value=record)
        producer.flush()

        _id += 1

        time.sleep(1)

"""

if producer is not None:
    while True:
        # Generate some abnormal observations
        if random.random() <= OUTLIERS_GENERATION_PROBABILITY:
            X_test = np.random.uniform(low=-4, high=4, size=(1, 2))
        else:
            X = 0.3 * np.random.randn(1, 2)
            X_test = (X + np.random.choice(a=[2, -2], size=1, p=[0.5, 0.5]))

        X_test = np.round(X_test, 3).tolist()

        current_time = datetime.utcnow().isoformat()

        record = {"id": _id, "data": X_test, "current_time": current_time}
        print(record)
        record = json.dumps(record).encode("utf-8")

        producer.produce(topic=TRANSACTIONS_TOPIC,
                         value=record)
        producer.flush()

        _id += 1
        time.sleep(DELAY)
"""