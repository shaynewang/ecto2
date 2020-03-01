import serial
import struct

class EctoSerial():
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

    def send(self, msg):
        """
        Args:
            msg: list [
                {'command1': Int32},
                {'command2': Int32},
                ...
            ]
        """
        with serial.Serial(
                self.port, self.baudrate, 
                bytesize=8, parity="N", stopbits=1) as ser:
            for d in msg:
                for command, val in d.items():
                    ser.write(command.encode())
                    ser.write(struct.pack("<i", val))

    def recv(self):
        pass
