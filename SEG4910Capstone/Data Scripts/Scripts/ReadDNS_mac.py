from scapy.all import *
import sys

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
def querysniff(pkt):
	if IP in pkt:
		ip_src = pkt[IP].src
		ip_dst = pkt[IP].dst
		if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
			query = str(pkt.getlayer(DNS).qd.qname).replace("'", "")[1:]

			print("'" + "{"+ '"Length"' + ":" + str(len(query)) 
			+ ', "Website"' + ":" + '"' + query + '"'
			+ ', "Subdomain length"' + ":" + str(getSubdomainLength(query)) 
			+ ', "Uppercase count"' + ":" + str(getUppercaseCount(query))   
			+ ', "Lowercase count"' + ":" + str(getLowercaseCount(query))  
			+ ', "Numeric count"' + ":" + str(getNumericCount(query))  
			+ ', "Entropy"' + ":" + str(getEntropyCount(query)) 
			+ ', "Special Char Count"' + ":" + str(getSpecialCharCount(query))  
			+ ', "Max label length"' + ":" + str(getLabelsMax(query)) 
			+ ', "Average label length"' + ":" + str(getLabelAvg(query))  
			+ ', "Number of Labels"' + ":" + str(getLabelNum(query)) 
			+ ', "Length of domain"' + ":" + str(getLengthDomain(query)) + "}" + "'")

            


sniff(iface = interface, filter = "port 53", prn = querysniff, store = 0)

