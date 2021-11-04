from googlesearch import search
import dns.resolver
import random, time
import pandas as pd
import re
from scapy.all import DNS, DNSQR, IP, sr1, UDP
import subprocess


def csv_reader(csv):

	df = pd.read_csv(csv)
	
	for item in df.values:
	
		myList = item[2].strip('][').split(', ')
		
		for i in myList:
			url = i.replace("'","")
			search(url)
			print(url)

csv_reader('complex_links[0-4992].csv')