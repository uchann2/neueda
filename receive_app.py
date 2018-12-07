import socket
import sys
import threading
import os
import json
from Crypto.Cipher import AES

host = ''   #Default is to receive files from any interface
port = 12345  # Default port
received_files = "./received" #Save received files to ./received folder by default
secret = ''
def loadconfig():
    with open('./config/receive_config.json', 'r') as f:
        config  = json.load(f)
    global host
    host = config['receive_host']
    global port
    port = config['receive_port']
    global received_files
    received_files = config ['received_files']
    global secret
    secret  = config['secret']
    f.close()

def handle_client(client_socket,client_addr):
    print('Connected by', client_addr)
    while True:
        filename = ''
        length = ''
        while True:
            try:
                data = client_socket.recv(1)
                if data == '|' or data == '': 
                    break
                filename =  filename + data
            except socket.error:
                print("Error Occured.")
        print(filename)
        while True:
            try:
                data = client_socket.recv(1)
                if data == '|' or data == '': 
                    break
                length =  length + data
            except socket.error:
                print("Error Occured.")
        print(length)
        if length != '':
            data = client_socket.recv(int(length))
        if data == '':
            break
        print(data)
        writetofile(filename,data)

def writetofile(filename,data):
        try:
            output = open(received_files+"/"+filename,"w+")
            output.write(data) 
            output.close()
        except:
            writetoconsole("Cannot write to file.")

if __name__ == "__main__":
    loadconfig()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, int(port)))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        client_handler = threading.Thread(target=handle_client,args=(conn,addr))
        client_handler.start()
    conn.close()