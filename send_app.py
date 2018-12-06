import socket
import os
import sys
import json
import dicttoxml
import threading

host = socket.gethostname()   #Default is to send files to localhost
port = 65530  # Default port
input_files = "./input" #Check for ./input folder by default
processed_files = "./xmls" #Save processed files to ./sent folder by default
sent_files = "./sent" #default location for sent files
secret = ''
bufferSize = 64 * 1024

def loadconfig():
    with open('./config/send_config.json', 'r') as f:
        config  = json.load(f)
    global host
    host = config['receive_host']
    global port
    port = config['receive_port']
    global input_files
    input_files = config ['input_files']
    global processed_files
    processed_files = config['processed_files']
    global secret
    secret  = config['secret']
    f.close()

def converttoxml(inputdir,processeddir):
    while True:
        processed = getprocessedxml(processeddir)
        for i in os.listdir(inputdir):
            if i.endswith('.json'):
                if i[0:-5] not in processed:
                    with open(inputdir+"/"+i, 'r') as f:
                        config  = json.load(f)
                    xml = dicttoxml.dicttoxml(config)
                    outputxml = open(processeddir+"/"+i[0:-5]+".xml","w")
                    outputxml.write(xml)
                    outputxml.close()
                    f.close()

# def encryptandsend(processeddir,sentdir,secret,bufferSize):
#     secret = "foopassword"
#     bufferSize = 64 * 1024
#     while True:
#         sent = getsent(sentdir)
#         for i in os.listdir(processeddir):
#             if i.endswith('.xml'):
#                 if i[0:-4] not in sent:
#                     source=processeddir+"/"+i
#                     dest=sentdir+"/"+i+".aes"
#                     pyAesCrypt.encryptFile(source, "data.txt.aes", password, bufferSize)

def getprocessedxml(processeddir):
    processed = []
    for i in os.listdir(processeddir):
        if i.endswith('.xml'):
            processed.append(i[0:-4])
    return processed

def getsent(sentdir):
    sent = []
    for i in os.listdir(sentdir):
        if i.endswith('.aes'):
            sent.append(i[0:-8])
    return sent
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, port))
# inputstring = 'Hello, world, hey yall second file'
# length = len(inputstring)
# sendstring = "File-2.txt|"+str(length)+"|"+ inputstring
# b = bytearray()
# b.extend(sendstring)
# s.sendall(b)
# s.close()

def sendtoremote(processeddir,sentdir,socket):
        sent = getsent(sentdir)
        for i in os.listdir(processeddir):
            if i.endswith('.xml'):
                if i[0:-5] not in sent:
                    with open(processeddir+"/"+i, 'r') as f:
                        content = f.read()
                        senddata = i+"|"+str(len(content))+"|"+content
                        b = bytearray()
                        b.extend(str(senddata))
                        socket.sendall(b)

if __name__ == "__main__":
    loadconfig()
    #convert_handler = threading.Thread(target=converttoxml,args=(input_files,processed_files))
    #convert_handler.start()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((host,int(port)))
    while True:
        sendtoremote(processed_files,sent_files,socket)
    socket.close()