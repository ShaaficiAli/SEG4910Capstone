import dns.resolver
import random, time
import pandas as pd
import re
from scapy.all import DNS, DNSQR, IP, sr1, UDP
import subprocess
import urllib
import requests 
#exclude a.root-servers.net
#exclude .html

#url_request python package
#prequest make get requests

#x=requests.get(url)
#print(x.status_code)

dns.resolver.nameservers = ['localhost']
csv = 'complex_links[0-4992].csv'


def dns_query_specific_nameserver(query, nameserver="1.1.1.1", qtype="AAAA"):
    """
    Query a specific nameserver for:
    - An IPv4 address for a given hostname (qtype="A")
    - An IPv6 address for a given hostname (qtype="AAAA")
    
    Returns the IP address as a string
    """
    process = subprocess.Popen(["nslookup", query], stdout=subprocess.PIPE)


def ping(url):
	try:
		if (url != ''):
			print(url)
			x = requests.get(url,timeout=10)
			print(x.status_code)
			#print(x.text+'\n')
	except requests.exceptions.Timeout:
		print("TIMEOUT")
		pass
	except requests.exceptions.ConnectionError:
		pass
	except dns.name.LabelTooLong:
		pass
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


csv_reader('complex_links[0-4992].csv')