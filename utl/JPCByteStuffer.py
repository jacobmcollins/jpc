# General Imports
import crc16
import json

# Project Imports
from utl.JPCProtocol import JPCProtocol


def append_crc(input):
    crc = calculate_crc(bytes(input))
    out = input + crc
    return out, crc


def remove_crc(input):
    crc = input[-2:]
    out = input[:-2]
    return out, crc


def calculate_crc(input):
    return crc16.crc16xmodem(bytes(input)).to_bytes(length=2, byteorder='little')


def byte_stuff(input):
    output = bytearray([])
    output.append(JPCProtocol.FRAME_BYTE[0])
    for byte in input:
        if byte == JPCProtocol.FRAME_BYTE[0] or byte == JPCProtocol.ESCAPE_BYTE[0]:
            output.append(JPCProtocol.ESCAPE_BYTE[0])
            output.append(byte ^ JPCProtocol.XOR_BYTE[0])
        else:
            output.append(byte)

    output.append(JPCProtocol.FRAME_BYTE[0])

    return output


def byte_unstuff(input):
    output = []
    length = len(input)
    data = bytearray([])

    i = 0
    while i in range(length):
        byte = input[i]
        if byte == JPCProtocol.FRAME_BYTE[0]:
            if len(data) != 0:
                output.append(data)
            data = bytearray([])
        elif byte == JPCProtocol.ESCAPE_BYTE[0]:
            i += 1
            byte = input[i]
            data.append(byte ^ JPCProtocol.XOR_BYTE[0])
        else:
            data.append(byte)
        i += 1

    return output


def get_valid_packets(input):
    output = []
    unstuffed = byte_unstuff(input)
    for packet in unstuffed:
        wo_crc, actual_crc = remove_crc(packet)
        expected_crc = calculate_crc(bytes(wo_crc))
        if actual_crc == expected_crc:
            output.append(wo_crc)
    return output


def byte_unstuff2(sock, do_stuff):
    data = bytearray([])
    byte = sock.recv(1)
    while byte:
        if byte == JPCProtocol.FRAME_BYTE:
            if len(data) != 0:
                do_stuff(data, sock)
            data = bytearray([])
        elif byte == JPCProtocol.ESCAPE_BYTE:
            byte = sock.recv(1)
            data.append(byte[0] ^ JPCProtocol.XOR_BYTE[0])
        else:
            x = byte[0]
            data.append(x)
        byte = sock.recv(1)
