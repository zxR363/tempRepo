import socket
import time
from dataclasses import dataclass
import random

def binarray(i):
    while i:
        yield i & 0xff
        i = i >> 8

def getHexValueList(val):
    tmp = [-1]
    for i in list(binarray(val)):
        tmp.append(i)
    return tmp

#print(getHexValueList(0x05BB))


def sendMessage(data):
    """
    while True:
        Message = input("Write a value:")
        my_str_as_bytes = str.encode(Message)

        clientSock.sendto(my_str_as_bytes, (UDP_IP_ADDRESS, UDP_PORT_NO))
    """
    for i in data:
        str_val = str(i)
        byte_val = str_val.encode()
        clientSock.sendto(byte_val, (UDP_IP_ADDRESS, UDP_PORT_NO))
        print(str_val)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#sendMessage("p")
#sendMessage("bc")

################################################################################################

@dataclass
class EntityID:
    site=[0,48]
    application = [0,1]
    entity = [0, 1]

@dataclass
class RadioID:
    radioID =[0,1]

@dataclass
class EncodingScheme:
    numberOfJWords=[0,11]

@dataclass
class TDLType:
    tdlType=[0,100]

@dataclass
class SampleRate:
    sampleRate = [0,0,0,0]

@dataclass
class DataLength:
    dataLength=[1,192]

@dataclass
class Samples:
    samples=[0]

@dataclass
class link16SignalPDU:
    npgNumber = [0,6]
    netNumber = [0]
    tsecCVLL=[255]
    msecCVLL=[255]
    messageTypeID=[0]
    padding=[0,0]
    timeSlotId=[0,0,0,0]
    perceivedTransmitTime=[255,255,255,255,255,255,255,255]

@dataclass
class MessageData:
    timeSlotType=[0,0,0,144]
    jwordFormat1 =[9,8,0,0]
    c2ind = [216,11,240,186]
    altitude = [0,0,255,228]  #Start Index => 51.Index
    parity=[0,0,0,0]
    jwordFormat2 =[44,107,75,42]
    latLon = [205,116,183,52] # Start Index => 63.Index
    jwordFormat3 = [53,5,0,5]
    modeCode = [146,0,114,7]
    airPlatform = [0,0,0,1]

  # Uzunluk 79 => 79 - 12 => Latlon Start Index = 67 - 4 => 63.Index  [4 Byte]
  # Altitude => Start Index = > 51.Index [4 Byte]



def appendMessage(message,data):
    if type(data)==list:
        for i in data:
            message.append(i)

message=[]


#Entity ID
for i in EntityID.site:
    message.append(i)
for i in EntityID.application:
    message.append(i)
for i in EntityID.entity:
    message.append(i)

#Radio ID
for i in RadioID.radioID:
    message.append(i)
#EncodingScheme
for i in EncodingScheme.numberOfJWords:
    message.append(i)
#TDLType
for i in TDLType.tdlType:
    message.append(i)

#SampleRate
for i in SampleRate.sampleRate:
    message.append(i)

#DataLength
for i in DataLength.dataLength:
    message.append(i)

#Samples
for i in Samples.samples:
    message.append(i)

#link16SignalPDU
for i in link16SignalPDU.npgNumber:
    message.append(i)
for i in link16SignalPDU.netNumber:
    message.append(i)
for i in link16SignalPDU.tsecCVLL:
    message.append(i)
for i in link16SignalPDU.msecCVLL:
    message.append(i)
for i in link16SignalPDU.messageTypeID:
    message.append(i)
for i in link16SignalPDU.padding:
    message.append(i)
for i in link16SignalPDU.timeSlotId:
    message.append(i)
for i in link16SignalPDU.perceivedTransmitTime:
    message.append(i)
#Message Data
for i in MessageData.timeSlotType:
    message.append(i)
for i in MessageData.jwordFormat1:
    message.append(i)
for i in MessageData.c2ind:
    message.append(i)
for i in MessageData.altitude:
    message.append(i)
for i in MessageData.parity:
    message.append(i)
for i in MessageData.jwordFormat2:
    message.append(i)
for i in MessageData.latLon:
    message.append(i)
for i in MessageData.jwordFormat3:
    message.append(i)
for i in MessageData.modeCode:
    message.append(i)
for i in MessageData.airPlatform:
    message.append(i)

print("Mesaj uzunlugu=",len(message))
print("Altitude StartIndex = ",message[51])
print("LatLon StartIndex = ",message[63])

while(True):
    #Alt
    message[53] = 255 - random.randint(0, 4)
    message[54] = 228 - random.randint(0, 3)
    #Lat Lon
    message[63] = 205 - random.randint(0, 6)
    message[64] = 116 - random.randint(0, 15)

    message[65] = 183 - random.randint(0, 6)
    message[66] = 52 - random.randint(0, 25)

    sendMessage(message)
    time.sleep(3)


#Altitude Examp:

"""
0000 FFE4 => 8992

89  <=>   92 Value

255   ,   228 

255 => (abs(255-val)* 100) % 500 + 8900
228 => (abs(228-val)* 3  + 92 ) % 100 => Sonuc

==> 

LAT  					LON
CD74 					B734 

205,116,				183 , 52

Val = 36.04 			Val = 139.90

205 => 36 				183 => 139
116 => 0.04			    52 => 0.90
"""