from scapy.all import *
import sys

import json
import random
import time
from datetime import datetime
import pandas as pd

import numpy as np

from settings import TRANSACTIONS_TOPIC, DELAY, OUTLIERS_GENERATION_PROBABILITY
from utils import create_producer

_id = 0

#DEPENDS ON YOUR COMPUTER, CHECK YOUR INTERFACES IN CMD LINE AND SET THIS VALUE TO THE APPROPRIATE INTERFACE
interface = "en0"

#Helper functions 
def getSubdomainLength(query):
	''
	labels = query.split('.')
	labels.pop()
	return sum(len(label) for label in labels)

def getUppercaseCount(query):
	return sum(1 for letter in query if letter.isupper())

def getLowercaseCount(query):
	return sum(1 for letter in query if letter.islower())

def getNumericCount(query):
	return sum(1 for letter in query if letter.isnumeric())

def getEntropyCount(query):
	'Returns Shannons entropy of a string'
	prob = [float(query.count(char)/len(query)) for char in dict.fromkeys(list(query))]
	entropy = -sum([p*math.log(p,2) for p in prob])
	return entropy

def getSpecialCharCount(query):
	return sum(1 for letter in query if (not letter.isalnum()))

def getLabelsMax(query):
	labels = query.split('.')
	return max(len(label) for label in labels)

def getLabelAvg(query):
	labels = query.split('.')
	sumlabel = sum(len(label) for label in labels)
	avglabel = sumlabel/len(labels)
	return avglabel

def getLabelNum(query):
	return len(query.split('.'))
  
def getLengthDomain(query):
	''
	labels = query.split('.')
	return len(labels.pop())


#Convert printed output to json
#print("{"+ '"length"' + ":" + '"' + str(len(query)) + '"' + "}")
#Sniff traffic, print features to console as a JSON string

packet = None

producer = create_producer()

def querysniff(pkt):
	if IP in pkt:
		ip_src = pkt[IP].src
		ip_dst = pkt[IP].dst
		if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
			query = str(pkt.getlayer(DNS).qd.qname).replace("'", "")[1:]
			data = [{'Length' : len(query), 'Subdomain length' : getSubdomainLength(query), 'Uppercase count' : getUppercaseCount(query),
			'Lowercase count': getLowercaseCount(query), 'Numeric count' : getNumericCount(query), 'Entropy' : getEntropyCount(query), 
			'Special Char Count' : getSpecialCharCount(query),'Max label length' : getLabelsMax(query), 'Average label length' : getLabelAvg(query), 
			'Number of Labels' : getLabelNum(query),'Length of domain' :getLengthDomain(query)}]

			current_time = datetime.utcnow().isoformat()
			record = {"id": 0, "data": data, "Website": query, "Timestamp": current_time}
			print(record)

			record = json.dumps(record).encode("utf-8")

			producer.produce(topic=TRANSACTIONS_TOPIC,
            value=record)
			producer.flush()



sniff(iface = interface, filter = "port 53", prn = querysniff, store = 0)

















