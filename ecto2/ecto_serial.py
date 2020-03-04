import serial
import struct

class EctoSerial():
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.last_sent = None
        self.ser = serial.Serial(port, baudrate,
                bytesize=8, parity="N", stopbits=1)

    def send(self, data):
        """
        Args:
            data: tuple (val1, val2)
        """
        d1 = struct.pack(">h", data[0])
        d2 = struct.pack(">h", data[1])
        msg = b"H"+d1+b":"+d2
        if self.last_sent != msg:
          self.ser.write(msg)
          self.last_sent = msg

    def recv(self):
        print("recv: ", self.ser.readline())
