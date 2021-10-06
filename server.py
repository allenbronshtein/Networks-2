import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '0.0.0.0'
server_port = int(sys.argv[1])
dict_files = {}
files_for_client = []
server.bind((server_ip, server_port))
server.listen(5)
while 1:
    client_socket, client_address = server.accept()
    print("Connection from: ", client_address)
    data = client_socket.recv(1024)
    dataD = data.decode()
    while not dataD == "":
        temp = dataD.split()
        status = temp[0]
        # upload files
        if status == '1':
            files = temp[2].split(',')
            dict_files[(client_address[0], temp[1])] = files
            print("Received:", dataD)
            data = client_socket.recv(1024)
            dataD = data.decode()
        # download files
        if status == '2':
            search_for = temp[1]
            for key in dict_files:
                # get all users files
                files = dict_files[key]
                for file in files:
                    s = file.split("/")
                    if search_for in s[-1]:
                        files_for_client.append((key, file))
            i = 0
            msg = ""
            for file in files_for_client:
                ip = file[0][0]
                port = str(file[0][1])
                msg += str(i + 1) + " " + file[1] + "," + ip + "," + port + "$"
                i += 1
            if msg == "":
                msg = "bad search"
            client_socket.send(msg.encode())
            dataD = ""
            files_for_client = []
    print("Client Disconnected")
