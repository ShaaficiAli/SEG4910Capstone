import os
import dns.resolver
import random, time
import pandas as pd
import re

dns.resolver.nameservers = ['localhost']

def mainLoop(url,it):

        types = ['NS', 'A', 'AAAA', 'MX']

        domain = url
        if(domain[0] != "."):
            rt = random.choice(types)
            print(domain,rt,it)
            try:
                dns.resolver.query(domain, rt)
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

def pingBenignData(frm,to):
    with open("/Users/filipbosnjak/Desktop/top-1m.csv") as file:
        WebsiteList = [line.strip('\n').split(",")[1] for line in file.readlines()]
    WebsiteList = WebsiteList[frm:to]
    i = 1
    for website in WebsiteList:
    	i = i+1
    	mainLoop(website,i)
    file.close()

pingBenignData(1,1000000)