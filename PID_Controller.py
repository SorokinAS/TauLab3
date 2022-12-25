import struct
from socket import *

reg = 0
error = []
for i in range(2):
    error.append(0)

def add_value(value, mas):
    mas.append(value)
    if len(mas) > 2:
        mas.pop(0)
    return mas

KP = 0.04
KI = 0.00001
KD = 0.9
SET_POINT = 500

PORT = 9031
HOST = 'localhost'
PORT_CTRL = 9101
PORT_SP = 9111

s = socket(AF_INET, SOCK_DGRAM)
s.bind((Host, Port))
sock = socket(AF_INET, SOCK_DGRAM)
while True:
    data, addr = s.recvfrom(1024)
    data = struct.unpack('d', data)[0]
    error = add_value(SET_POINT - data, error)
    pid_ctrl = KP * error[1] + KI * (reg+error[1]) + KD * (error[1]-error[0])
    reg = reg + error[1]
    mes = struct.pack('d', pid_ctrl)
    sock.sendto(mes, (HOST, PORT_CTRL))
    mes_sp = struct.pack('d', SET_POINT)
    sock.sendto(mes_sp, (Host, Port_sp))
