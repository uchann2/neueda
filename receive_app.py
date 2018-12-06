import socket
import sys
import threading
import os

host = ''   #Default is to receive files from any interface
port = 12345  # Default port
received_files = "./received" #Save received files to ./received folder by default

def handle_client(client_socket,client_addr):
    print('Connected by', client_addr)
    msg = ''
    filename = ''
    length = ''
    while True:
        try:
            data = client_socket.recv(1)
            if data == '|': 
                break
            filename =  filename + data
        except socket.error:
            print "Error Occured."
    while True:
        try:
            data = client_socket.recv(1)
            if data == '|': 
                break
            length =  length + data
        except socket.error:
            print "Error Occured."
    output = open(received_files+"/"+filename,"w+")
    while True:
        try:
            data = client_socket.recv(int(length))
            if not data:
                break
            output.write(data)
        except socket.error:
            print "Error Occured."
            break
    output.close()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        client_handler = threading.Thread(target=handle_client,args=(conn,addr))
        client_handler.start()
    conn.close()