from socket import socket, AF_INET, SOCK_STREAM, SHUT_WR
import sys
import glob

s = socket(AF_INET, SOCK_STREAM)
status = int(sys.argv[1])
dest_ip = sys.argv[2]
dest_port = int(sys.argv[3])
dataD = ""
# client is sharing files
if status == 0:
    client_listen_port = int(sys.argv[4])
    s.connect((dest_ip, dest_port))
    files = glob.glob("/home/allen/Desktop/ex2/*.*")
    data = "1 " + str(client_listen_port) + " "
    for item in files:
        data += item + ","
    print(data)
    s.send(data.encode())
    s.send(''.encode())
    s.close()
    # now server
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('0.0.0.0', client_listen_port))
    s.listen(5)
    while 1:
        client_socket, client_address = s.accept()
        print("Connection from: ", client_address)
        data = client_socket.recv(1024)
        with open(data, "rb") as f:
            content = f.read(1024)
            client_socket.send(content)
            while content:
                content = f.read(1024)
                client_socket.send(content)
        f.close()
        client_socket.close()
# client is downloading files
elif status == 1:
    file_details = []
    dataD = ""
    while not dataD == 'quit':
        # Request file from server
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((dest_ip, dest_port))
        msg = input("Search: ")
        data = "2 " + msg
        s.send(data.encode())
        data = s.recv(1024)
        dataD = data.decode()
        if dataD == "bad search":
            print(dataD)
            continue
        file_details = dataD.split("$")
        for_print = ""
        for details in file_details[:-1]:
            temp = details.split(",")
            for_print = for_print + temp[0] + ","
        print(for_print[:-1])
        msg = input("Choose file: ")
        my_file = file_details[int(msg) - 1]
        server_details = my_file.split(",")
        # closed connection with server
        s.close()

        # open connection with client-server
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((server_details[1], int(server_details[2])))
        s.send(server_details[0][2:].encode())
        data = s.recv(1024)
        with open(server_details[1], "wb") as f:
            while data:
                f.write(data)
                data = s.recv(1024)
        f.close()
        s.close()
        # closed connection with client-server
s.close()
