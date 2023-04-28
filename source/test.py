import socket


sock =  socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.settimeout(1)
sock.bind(("34:6F:24:A5:6E:28", 30))
sock.listen(100)
sock.setblocking(False)
try:
    sock, addr = sock.accept()
except:
    pass
sock.close()

