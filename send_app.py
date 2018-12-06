import socket
import os
import sys
import json
import dicttoxml


host = socket.gethostname()   #Default is to send files to localhost
port = 65530  # Default port
input_files = "./input" #Check for ./input folder by default
processed_files = "./sent" #Save processed files to ./sent folder by default
secret = ''

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

def converttoxml():
    processed = getprocessedxml()
    for i in os.listdir(input_files):
        if i.endswith('.json'):
            if i[0:-5] not in processed:
                with open(input_files+"/"+i, 'r') as f:
                    config  = json.load(f)
                xml = dicttoxml.dicttoxml(config)
                outputxml = open(processed_files+"/"+i[0:-5]+".xml","w")
                outputxml.write(xml)
                outputxml.close()
                f.close()

def getprocessedxml():
    processed = []
    for i in os.listdir(processed_files):
        if i.endswith('.xml'):
            processed.append(i[0:-4])
    return processed
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, port))
# inputstring = 'Hello, world, hey yall second file'
# length = len(inputstring)
# sendstring = "File-2.txt|"+str(length)+"|"+ inputstring
# b = bytearray()
# b.extend(sendstring)
# s.sendall(b)
# s.close()

if __name__ == "__main__":
    loadconfig()
    converttoxml()