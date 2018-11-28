# General Imports
import socket
import time

# Project Imports
from utl.JPCProtocol import JPCProtocol
from utl.JPCByteStuffer import get_valid_packets


class ReconnectingSocket:
    def __init__(self, server_address):
        self.address = server_address
        self.sock = None
        self.connected = False
        self.buffer = b''
        self.last_heartbeat = 0

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.sock.connect_ex((self.address, JPCProtocol.STANDARD_PORT)) != 0:
            time.sleep(1)
        self.connected = True
        self.last_heartbeat = time.time()

    def disconnect(self):
        if self.sock:
            self.sock.detach()
        self.sock = None
        self.connected = False
        self.last_heartbeat = 0

    def reconnect(self):
        self.disconnect()
        self.connect()

    def send(self, raw_data):
        if self.connected:
            self.sock.send(raw_data)

    def recv(self):
        if self.connected:
            data = self.sock.recv(9999999)
            packet_list = get_valid_packets(data)
            return packet_list

    def update_heartbeat(self, t):
        self.last_heartbeat = t
