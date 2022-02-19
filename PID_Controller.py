import struct
from socket import *

reg = 0
error = []
for i in range(2):
    error.append(0)

def addValue(value, mas):
    mas.append(value)
    if len(mas) > 2:
        mas.pop(0)
    return mas

kp = 0.04
ki = 0.00001
kd = 0.9
set_point = 500

Port = 9031
Host = 'localhost'
Port_ctrl = 9101
Port_sp = 9111

s = socket(AF_INET, SOCK_DGRAM)
s.bind((Host, Port))
sock = socket(AF_INET, SOCK_DGRAM)
while True:
    data, addr = s.recvfrom(1024)
    data = struct.unpack('d', data)[0]
    error = addValue(set_point - data, error)
    pid_ctrl = kp * error[1] + ki * (reg+error[1]) + kd * (error[1]-error[0])
    reg = reg + error[1]
    mes = struct.pack('d', pid_ctrl)
    sock.sendto(mes, (Host, Port_ctrl))
    mes_sp = struct.pack('d', set_point)
    sock.sendto(mes_sp, (Host, Port_sp))
