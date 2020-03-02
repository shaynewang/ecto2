import serial
import struct

class EctoSerial():
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.last_sent = None

    def send(self, data):
        """
        Args:
            data: tuple (val1, val2)
        """
        with serial.Serial(
                self.port, self.baudrate, 
                bytesize=8, parity="N", stopbits=1) as ser:
            d1 = str(data[0])
            d2 = str(data[1])
            d1 = struct.pack("<i", data[0])
            d2 = struct.pack("<i", data[1])
            msg = b"<"+d1+b":"+d2+b">"
#            msg = msg.encode()
            if self.last_sent != msg:
              print(msg)
              print(ser.write(msg))
              self.last_sent = msg

    def recv(self):
        with serial.Serial(
                self.port, self.baudrate, 
                bytesize=8, parity="N", stopbits=1,timeout=1) as ser:
            print("recv: ", ser.readline())
