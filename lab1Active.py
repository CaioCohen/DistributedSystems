import socket

def ativoSocket():
    HOST = '10.11.0.14'
    PORTA = 5000

    sock = socket.socket()
    
    sock.connect((HOST,PORTA))
    sock.send(b"Ola, sou o lado ativo")
    msg = sock.recv(1024).decode()

    print(str(msg))

    sock.close()

ativoSocket()