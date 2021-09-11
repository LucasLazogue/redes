import socket
import threading as th


def recibirRespuesta():
    msg = ""
    while '\n' not in msg:
        msg += s.recv(1024).decode("utf-8")
    if msg == 'OK\n':
        print("OK")
    else:
        print(msg)
    #AGREGO RETURN PARA PROBAR
    return msg


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 2021))

nombre = input("Ingrese un nombre: ")
s.send(bytes("PLAYER " + nombre + '\n', "utf-8"))
recibirRespuesta()

puerto = input("Ingrese número de puerto: ")
s.send(bytes("LISTEN " + puerto + '\n', "utf-8"))


# LUCAS

def server_mundo(mundo):
    while True:
        data, addr = mundo.recvfrom(1024)
        print(data.decode("utf-8"))


udp = input("ENTER PARA MANDAR PRIMER UDP: ")
s.send(bytes("UDP" + '\n', "utf-8"))
mundo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mundo.bind((socket.gethostname(), int(puerto)))
thread = th.Thread(target=server_mundo, args=(mundo,))
thread.start()

msg = ''
while msg != 'fin':
    msg = input("MENSAJE - FIN PARA FINALIZAR: ")
    if msg == '':
        s.send(bytes(msg + '\n', "utf-8"))
mundo.close()
s.close()

