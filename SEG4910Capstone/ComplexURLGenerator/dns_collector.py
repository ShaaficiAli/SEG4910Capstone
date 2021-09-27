import dns.resolver
import random, time
import pandas as pd
import re

dns.resolver.nameservers = ['localhost']
csv = 'complex_links[0-4992].csv'

df = pd.read_csv('complex_links[0-4992].csv')

def ping(url):

	types = ['NS', 'A', 'AAAA', 'MX']
	rt = random.choice(types)

	try:
		dns.resolver.query(url, rt)
	except dns.resolver.NXDOMAIN:
		pass
	except dns.resolver.NoAnswer:
		pass
	except dns.resolver.Timeout:
		pass
	except dns.resolver.YXDOMAIN:
		pass
	except dns.resolver.NoNameservers:
		pass

def csv_reader(csv):

	df = pd.read_csv(csv)
	
	for item in df.values:
	
		myList = item[2].strip('][').split(', ')
		
		for i in myList:
				url = i.replace("'","")
				ping(url)

