# General Imports
import json
import time
from uuid import getnode as get_mac

# Project Imports
from utl.JPCByteStuffer import append_crc, byte_stuff
from utl.JPCProtocol import JPCProtocol
from utl.JPCLogging import JPCLogger


class JPCPacket:
    opcode = None
    payload = None

    def to_json(self):
        obj = {'opcode': self.opcode, 'payload': self.payload}
        return json.dumps(obj)

    def send(self, recipient):
        json_str = self.to_json()
        json_bytes = bytearray(json_str.encode())
        JPCLogger.log_tx(json_str, time.time())
        with_crc, crc = append_crc(json_bytes)
        stuffed = byte_stuff(with_crc)
        recipient.send(stuffed)


class JPCHelloPacket(JPCPacket):
    def __init__(self):
        self.opcode = JPCProtocol.HELLO
        self.payload = get_mac()


class JPCHeartbeatPacket(JPCPacket):
    def __init__(self):
        self.opcode = JPCProtocol.HEARTBEAT
        self.payload = get_mac()


class JPCTellTextPacket(JPCPacket):
    def __init__(self, message, recipient):
        self.opcode = JPCProtocol.TELL
        self.payload = {'message_type': JPCProtocol.MESSAGE_TEXT, 'recipient': recipient, 'message': message}

class JPCTellImagePacket(JPCPacket):
    def __init__(self, image, recipient):
        self.opcode = JPCProtocol.TELL
        self.payload = {'message_type': JPCProtocol.MESSAGE_IMG, 'recipient': recipient, 'message': image}

class JPCTellPacketFactory:
    def get(message_type, message, recipient):
        if message_type == JPCProtocol.MESSAGE_TEXT:
            return JPCTellTextPacket(message, recipient)
        elif message_type == JPCProtocol.MESSAGE_IMG:
            return JPCTellImagePacket(message, recipient)

