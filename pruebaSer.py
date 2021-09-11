import socket
import threading as th
import re
import time

PLAYERS = []


def servidor(PORT):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(("", PORT))
  s.listen()
  print("Servidor corriendo")

  while True:
    client, address = s.accept()

    thread = th.Thread(target=atenderCliente, args=(client,))
    thread.start()
  s.close()


def login(client, msg):
  msg = msg.split()
  if len(msg) == 2 and msg[1] not in PLAYERS and re.match('^\w+$', msg[1]):
    PLAYERS.append(msg[1])
    print(PLAYERS)
    client.send(bytes('OK\n', "utf-8"))
    return msg[1]
  # Caso de error donde no hay nombre
  elif len(msg) == 1:
    client.send(bytes('FAIL 001:Nombre_vacio\n', "utf-8"))
  # Caso de error donde el nombre ya está tomado
  elif msg[1] in PLAYERS:
    client.send(bytes('FAIL 002:Nombre_ocupado\n', "utf-8"))
  # Caso de error donde el nombre tiene espacios
  elif len(msg) > 2:
    client.send(bytes('FAIL 003:Nombre_con_espacios\n', "utf-8"))
  # Caso de error donde hay caracteres no alfanumericos en el nombre
  else:
    client.send(bytes('FAIL 004:Nombre_con_caracteres_no_alfanumericos\n', "utf-8"))
  return None


def listen(client, msg):
  msg = msg.split()
  if len(msg) == 2 and re.match('^\d+$', msg[1]) and int(msg[1]) <= 65536:
    print(msg[1])
    client.send(bytes('OK\n', "utf-8"))
    return msg[1]
  # Caso de error donde no hay puerto
  elif len(msg) == 1:
    client.send(bytes('FAIL 005:Puerto_vacio\n', "utf-8"))
  # Caso de error donde no es un número de puerto
  else:
    client.send(bytes('FAIL 006:No_es_un_numero_de_puerto\n', "utf-8"))
  return None


def datos_mundo(client, host, portnumber):
  while True:
    client.sendto(bytes('SEE\n', "utf-8"), (host, int(portnumber)))
    time.sleep(10)


def atenderCliente(client):
  msg = ""
  fin = False
  #AGREGO ESTO PARA SOLO ENTRAR AL THREAD UNA VEZ
  udp = False

  while (not fin):
    while '\n' not in msg:
      msg += client.recv(1024).decode("utf-8")
      if len(msg) == 0: break
    if 'PLAYER' in msg:
      username = login(client, msg)
      if username == None: fin = True
    elif 'LISTEN' in msg:
      portnumber = listen(client, msg)
      if portnumber == None: fin = True
      # LUCAS - ENVIO DE MENSAJES UDP
      # QUIERO ENVIAR LOS DATOS POR LA CONEXION TCP AL SOCKET UDP PERO NO LO RECIBE
    elif 'UDP' and not udp:
      print("ENTRO UDP")
      udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      host, port = client.getpeername()
      print('host: ' + host)
      print('port:' + portnumber)
      thread = th.Thread(target=datos_mundo, args=(udp_socket, host, portnumber))
      thread.start()


    if len(msg) == 0:
      fin = True
    msg = ""
  if username != None:
    PLAYERS.remove(username)


servidor(2021)