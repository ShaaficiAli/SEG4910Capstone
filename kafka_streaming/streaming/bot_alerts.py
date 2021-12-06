import json
import logging

from settings import SLACK_API_TOKEN, SLACK_CHANNEL, ANOMALIES_TOPIC, ANOMALIES_CONSUMER_GROUP
from utils import create_consumer


consumer = create_consumer(topic=ANOMALIES_TOPIC, group_id=ANOMALIES_CONSUMER_GROUP)

while True:
    print("Test")
    message = consumer.poll()
    print(message)
    if message is None:
        continue
    if message.error():
        logging.error("Consumer error: {}".format(message.error()))
        continue

    # Message that came from producer
    record = message.value().decode('utf-8')
    print(record)

    """
    try:
        # Send message to slack channel
        response = client.chat_postMessage(channel=SLACK_CHANNEL,
                                           text=record)
    except SlackApiError as e:

        print(e.response["error"])
     """

    #consumer.commit()

consumer.close()
