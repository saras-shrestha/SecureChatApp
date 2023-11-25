import socket
import threading
import pickle

# Connection Data
host = '127.0.0.1'
port = 12345
# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients_connected = []
nicknames = []
clients_pkey=[]
# clients_data={}

BUFFER_SIZE=4096

# Sending Messages To All Connected Clients
def broadcast(message, client):
    try:
        for c in clients_connected:
            #print(f'client is {c}')
            if c != client:
                c.send(message)
                # print(f"IC->{message}")
    except:
        print("Board Error")
# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(BUFFER_SIZE)
            broadcast(message, client)
        except:
            clients_connected.remove(client)
            client.close()
            break
def shareKey():
    for c in clients_connected:
        for k in clients_pkey:
                if(clients_pkey.index(k)==clients_connected.index(c)):
                    continue
                # uname = nicknames[k].encode('utf-8')
                # sep=b'##$$##'
                # g_msg=uname+sep+k
                # print(g_msg)
                ss=c.send(k)
                print(f"Broad{k}and {c}")
# def shareName():
#     for c in clients_connected:
#         for k in nicknames:
#             if (clients_pkey.index(k) == clients_connected.index(c)):
#                 continue
#             c.send(k.encode('utf-8'))
#             print(f"Broad{k}and {c}")


# Receiving / Listening Function
def receive():
    while True:
        client, address = server.accept()
        print(f"Connections from {address} has been established")

        try:
            rmsg = client.recv(1024)
            client.send('NICK'.encode('utf-8'))
            client_name = client.recv(1024).decode('utf-8')
            print(f"{address} identified itself as {client_name}")
            clients_connected.append(client)
            nicknames.append(client_name)
            clients_pkey.append(rmsg)
            # for sharing public key
            if(len(clients_connected)==2):
                shareKey()
                # shareName()
        except:
            print(f"{address} disconnected")
            client.close()
            continue

        thread1 = threading.Thread(target=handle, args=(client,))
        thread1.start()
print('Server Running....!')

receive()