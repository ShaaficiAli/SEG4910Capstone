
import pandas as pd 
from bs4 import BeautifulSoup, SoupStrainer
import requests
import regex as re
import socket
import os
import errno
from time import sleep


'''
pip3 install "requests[security]"
pip3 install pathlib
pip3 install ruamel_yaml 
pip3 install --upgrade certifi
'''

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
#Reading CSV of top 1 million links into pandas dataframe
url_list = pd.read_csv('top1m.csv')
#Removing indexes from datafram
url_list = url_list.drop(url_list.columns[0], axis=1)


#@timeout(2, os.strerror(errno.ETIMEDOUT))
def get_links(url):
	'''
	Takes a url in string form as input
	Returns 
		simple_links
			list of all links that DO NOT have a uppercase letter or digit
		compl_links
			list of all links that DO have either a uppercase or digit 
	'''
	simple_links = []
	compl_links = []

	headers = requests.utils.default_headers()

	headers.update(
    	{
        	'User-Agent': 'My User Agent 1.0',
    	}
	)	

	try:
		page = requests.get(url,headers=headers,timeout=10)
	except requests.exceptions.ConnectionError:
		print('Handle CONNECTION ERROR Exception')
		return [],[]
	except requests.exceptions.Timeout:
		print('Handle TIMEOUT Exception')
		return [],[]
	except requests.Timeout as err:
		print('Handle TIMEOUT Exception')
		return [],[]
	except requests.exceptions.TooManyRedirects:
		print('Handle REDIRECT Exception')
		return [],[]

	data = page.text
	soup = BeautifulSoup(data)

	for link in soup.find_all('a'):
		link = str(link.get('href'))

		if(bool(re.match(r'\w*[A-Z]\w*', link)) or bool(re.match(r'.*[0-9].*', link))):
			if('http' in link):
				compl_links.append(link)
		else:
			if('http' in link):
				simple_links.append(link)

	return simple_links,compl_links

def generator(df):

	df_new = pd.DataFrame(columns=['URL','COMPLEX_LINKS','SIMPLELINKS'])
	counter = 0

	for url in df.values:
		

		print(url)
		url = 'http://'+url[0]
		

		l1,l2 = get_links(url)
		
		print(l2)

		df_to_add = pd.DataFrame({'URL':url,'COMPLEX_LINKS':[l2],'SIMPLELINKS':[l1]})
		df_new = df_new.append(df_to_add)

		if(counter % 10 == 0):
			df_new.to_csv('complex_links.csv', index=True)
		counter = counter + 1

generator(url_list)








