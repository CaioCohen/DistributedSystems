import socket

def ativoSocket():
    HOST = 'localhost'
    PORTA = 5000

    sock = socket.socket()
    
    sock.connect((HOST,PORTA))
    msg = ""
    while True:
        msg = input()
        if msg == 'fim':
            break
        sock.send(msg.encode('utf-8'))
        retorno = sock.recv(1024).decode()
        print(str(retorno))

    sock.close()

ativoSocket()