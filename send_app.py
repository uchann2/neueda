import socket

host = socket.gethostname()
port = 12346                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
inputstring = 'Hello, world, hey yall'
length = len(inputstring)
sendstring = "File-1.txt|"+str(length)+"|"+ inputstring
b = bytearray()
b.extend(sendstring)
s.sendall(b)
s.close()