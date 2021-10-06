import socket,sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
msg = MESSAGE*10
s.send(msg.encode())
s.send(msg.encode())
s.send(msg.encode())
s.send(msg.encode())
data = s.recv(BUFFER_SIZE)
dataD = data.decode()
s.close()

print ("received data:", dataD)

