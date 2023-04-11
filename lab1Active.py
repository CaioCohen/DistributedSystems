import socket

def ativoSocket():
    HOST = 'localhost'
    PORTA = 5000

    sock = socket.socket()
    
    sock.connect((HOST,PORTA))
    sock.send(b"Ola, sou o lado ativo")
    msg = sock.recv(1024)

    print(str(msg, enconding='utf-8'))

    sock.close()