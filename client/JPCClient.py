# General Imports
import binascii
import json
import socket
import time

# Project Imports
from client.JPCClientGUI import JPCClientGUI
from client.ReconnectingSocket import ReconnectingSocket
from utl.JPCError import JPCHeartbeatTimeout
from utl.JPCLogging import JPCLogger
from utl.JPCPacket import JPCHelloPacket, JPCHeartbeatPacket
from utl.JPCProtocol import JPCProtocol


# Pi3 Client Class
class JPCClient:
    def __init__(self, server_address):
        # Create GUI
        self.gui = JPCClientGUI()
        self.gui.start()

        # Create server connection
        self.server = ReconnectingSocket(server_address)
        self.server.connect()
        print('about to send hello')
        self.send_hello()
        self.send_heartbeat()

    def send_hello(self):
        packet = JPCHelloPacket()
        packet.send(self.server)

    def send_heartbeat(self):
        packet = JPCHeartbeatPacket()
        packet.send(self.server)

    def run(self):
        try:
            while True:
                self.handle_heartbeats(time.time())
                self.process_packets()
                self.gui.root.update()
        except JPCHeartbeatTimeout:
            print('hrtbt timeout')
        except socket.error:
            print('socket error')
        except:
            print('idk')
        finally:
            self.re_run()

    def process_packets(self):
        packets = self.server.recv()
        for packet in packets:
            json_data = json.loads(packet.decode('utf-8'))
            JPCLogger.log_rx(json_data, time.time())
            self.process(json_data)

    def handle_heartbeats(self, t):
        elapsed = self.server.last_heartbeat - t
        if self.server.connected and elapsed >= JPCProtocol.HEARTBEAT_INTERVAL:
            self.send_heartbeat()
            if elapsed >= JPCProtocol.HEARTBEAT_TIMEOUT:
                raise JPCHeartbeatTimeout

    def re_run(self):
        self.server.reconnect()
        self.send_hello()
        self.send_heartbeat()
        self.run()

    def process(self, data):
        opcode = data['opcode']
        payload = data['payload']

        switcher = {
            JPCProtocol.TELL:       self.process_tell,
            JPCProtocol.ERROR:      self.process_error,
            JPCProtocol.HEARTBEAT:   self.process_heartbeat
        }

        switcher[opcode](payload)

    def process_tell(self, payload):
        try:
            message = payload['message']
            message_type = payload['message_type']
            if message_type == JPCProtocol.MESSAGE_TEXT:
                print('rx a text message')
                self.process_tell_text(message)
            elif message_type == JPCProtocol.MESSAGE_IMG:
                print('rx an image')
                self.process_tell_image(message)
        except:
            print("failed")

    def process_tell_text(self, message):
        self.gui.set_message(message)

    def process_tell_image(self, image):
        hex = binascii.unhexlify(image.encode('utf-8'))
        with open("temp", "wb") as file:
            file.write(hex)
        self.gui.set_image("temp")

    def process_error(self, error_code):
        if error_code == JPCProtocol.ERROR_TIMED_OUT:
            self.close()
            return False

    def process_heartbeat(self, payload):
        self.server.update_heartbeat(time.time())
        self.send_heartbeat()

    def send(self, msg):
        JPCProtocol(JPCProtocol.SEND, msg).send(self.server)

    def close(self):
        self.server.close()

