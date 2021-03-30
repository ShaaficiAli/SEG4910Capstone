import dns.resolver
import random, time
import pandas as pd
import re
dns.resolver.nameservers = ['localhost']

def getDomain(csv):

        df = pd.read_csv(csv)

        rndm = df.sample()
        domain = rndm["Root Domain"]
        domain_string = pd.Series.to_string(domain)
        newstring = re.sub(r"[^a-zA-Z\.]+", "",domain_string)
        return newstring

def getDomain1M(csv):

        df = pd.read_csv(csv)
        df.columns =['Number', 'URL']
        rndm = df.sample()
        url = rndm['URL']
        url_str = pd.Series.to_string(url)
        print(url_str)
        newstring = re.sub(r"[^a-zA-Z\.]+", "",url_str)
        return newstring

def mainLoop():

        types = ['NS', 'A', 'AAAA', 'MX']

        while True:

                domain = getDomain1M("top1m.csv")
                if(domain[0] != "."):
                        rt = random.choice(types)
                        print(domain,rt)
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
                        time.sleep(0.01)

mainLoop()