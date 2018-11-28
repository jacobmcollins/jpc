# General Imports
import binascii
import json
import socket
import threading
import time

# Project Imports
from server.JPCUser import JPCUserList
from utl.JPCByteStuffer import get_valid_packets
from utl.JPCError import JPCHeartbeatTimeout
from utl.JPCProtocol import JPCProtocol
from utl.JPCLogging import JPCLogger


class JPCServer:
    def __init__(self):
        self.users = JPCUserList("pi_whitelist.txt")
        threading.Thread(target=self.users.tx_rx_heartbeats).start()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind(('localhost', JPCProtocol.STANDARD_PORT))

    def send_image(self, image_file, recipient):
        file = open(image_file, "rb")
        buff = file.read()
        hex_data = binascii.hexlify(buff)
        str_data = hex_data.decode('utf-8')
        self.users.send_message(JPCProtocol.MESSAGE_IMG, str_data, recipient)

    def send_message(self, message, recipient):
        self.users.send_message(JPCProtocol.MESSAGE_TEXT, message, recipient)

    def run(self):
        self.connection.listen(5)
        while True:
            connection, client_address = self.connection.accept()
            threading.Thread(target=self.handle, args=[connection]).start()

    def handle(self, connection):
        try:
            running = True
            while running:
                data = connection.recv(64000)
                if data:
                    packets = get_valid_packets(data)
                    for packet in packets:
                        json_data = json.loads(packet)
                        JPCLogger.log_rx(json_data, time.time())
                        self.process(json_data, connection)
        except JPCHeartbeatTimeout:
            print('hrtbt timeout')
        except:
            pass


    def process(self, data, connection):
        opcode = data['opcode']
        payload = data['payload']

        switcher = {
            JPCProtocol.HELLO:      self.process_hello,
            JPCProtocol.HEARTBEAT:  self.process_heartbeat,
        }

        switcher[opcode](payload, connection)

    def process_hello(self, payload, s):
        self.users.update_heartbeat(payload)
        self.users.establish(payload, s)

    def process_heartbeat(self, payload, s):
        self.users.update_heartbeat(payload)

