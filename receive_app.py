import socket
import sys
import threading

host = ''        # Symbolic name meaning all available interfaces
port = 12345     # Arbitrary non-privileged port

def handle_client(client_socket,client_addr):
    print('Connected by', client_addr)
    while True:
        try:
            data = client_socket.recv(1024)
            if not data: break
            print "Client Says: "+data
            conn.sendall("Server Says:hi")

        except socket.error:
            print "Error Occured."
            break

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        client_handler = threading.Thread(target=handle_client,args=(conn,addr))
        client_handler.start()
    conn.close()