**Data Generation Process**

1.  We got a top million Alexa domains

2.  We use url generator to generate complex links from those domains:</br>
    Run command "python3 url_gen.py"
   
3.  Then we generate all the complex and simples link on a file</br>
    Filename: "complex_links.csv"
    
5.  Before generate DNS query, we use TCPDump to capture Traffic</br>
    Run command "sudo tcpdump port 53 -w test.pcap"</br>
    Then at the end, all the dns queries will be in the test.pcap file
    
4.  Generate DNS query data from the complex links created</br>
    Run command "python3 url_gen.py"
