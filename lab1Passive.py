import socket

HOST = ''
PORTA = 5000 

sock = socket.socket()
sock.bind((HOST, PORTA))  

conn, address = sock.accept()
sock.listen(5)
print("Connection from: " + str(address))
while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print("from connected user: " + str(data))
    conn.send(b'Ola, sou o lado passivo')

conn.close()  
sock.close()


