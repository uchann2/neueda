# coding: utf-8
import socket
import os
import sys
import json
import dicttoxml
import threading
from Crypto.Cipher import AES

host = "127.0.0.1"  #Default is to send files to localhost
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

def converttoxml(inputdir,processeddir,socket):
    while True:
        processed = getprocessedxml(processeddir)
        for i in os.listdir(inputdir):
            if i.endswith('.json'):
                if i[0:-5] not in processed:
                    with open(inputdir+"/"+i, 'r') as f:
                        try:
                            config  = json.load(f)
                        except ValueError:
                            print("retrying")
                            break
                    xml = dicttoxml.dicttoxml(config)
                    encdata = str(encryptdata(xml))
                    senddata = i[0:-5]+".xml"+"|"+str(len(xml))+"|"
                    b = bytearray()
                    b.extend(str(senddata))
                    b.extend(encdata)
                    socket.sendall(b)
                    outputxml = open(processeddir+"/"+i[0:-5]+".xml","wb")
                    outputxml.write(encdata)
                    outputxml.close()
                    f.close()

def encryptdata(data):
    encryption_suite = AES.new(secret, AES.MODE_CBC, 16 * '\x00')
    cipher_text = encryption_suite.encrypt(data)
    print(cipher_text)
    return cipher_text

def getprocessedxml(processeddir):
    processed = []
    for i in os.listdir(processeddir):
        if i.endswith('.xml'):
            processed.append(i[0:-4])
    return processed

if __name__ == "__main__":
    loadconfig()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((host,int(port)))
    converttoxml(input_files,processed_files,socket)
    socket.close()