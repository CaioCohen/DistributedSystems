import socket

HOST = 'localhost'
PORTA = 5000 

sock = socket.socket()
sock.bind((HOST, PORTA))  

sock.listen(5)
conn, address = sock.accept()
print("Adress: " + str(address) + "Connection: " + str(conn))
while True:
    data = conn.recv(1024).decode()
    if (not data):
        break
    print("Veio do lado ativo: " + str(data))
    conn.send(data.encode('utf-8'))

conn.close()
sock.close()


