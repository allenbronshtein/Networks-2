import socket,sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER_SIZE)
dataD = data.decode()
print ("received data:", dataD)
data = s.recv(BUFFER_SIZE)
dataD = data.decode()
print ("received data:", dataD)
s.close()



