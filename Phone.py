import time
from socket import *

gPort = 31337
NumberOfPixels = 390
################################################################################
def MakePixel(Red, Green, Blue):
  return chr(Red) + chr(Green) + chr(Blue)

################################################################################
def SendPacket(Socket, Packet):
  Socket.sendto(Packet, ('workroom-partylights.internal.sbhackerspace.com', gPort))
  Socket.sendto(Packet, ('classroom-partylights.internal.sbhackerspace.com', gPort))
  Socket.sendto(Packet, ('10.18.0.68', gPort))

################################################################################
def triggerPhone():
  Socket = socket(AF_INET, SOCK_DGRAM)
  Socket.bind(('', 0))
  Socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
  for i in range(8):
    Packet = MakePixel(0, 255, 0) * NumberOfPixels
    SendPacket(Socket, Packet)
    time.sleep(.8)
    Packet = MakePixel(0, 0, 0) * NumberOfPixels
    SendPacket(Socket, Packet)
    time.sleep(.4)
