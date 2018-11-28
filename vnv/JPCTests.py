# General Imports
import socket
import unittest
import threading

# Project Imports
from utl.JPCByteStuffer import *
from utl.JPCProtocol import JPCProtocol


class TestJPCByteStuffer(unittest.TestCase):

    def test_byte_stuff(self):
        stuffed = bytearray([
            JPCProtocol.FRAME_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            JPCProtocol.FRAME_BYTE ^ JPCProtocol.XOR_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            JPCProtocol.ESCAPE_BYTE ^ JPCProtocol.XOR_BYTE,
            0xFF,
            JPCProtocol.FRAME_BYTE
        ])

        unstuffed = bytearray([
            0xFF,
            JPCProtocol.FRAME_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            0xFF
        ])

        expected = stuffed
        actual = byte_stuff(unstuffed)
        self.assertEqual(expected, actual)

    def test_byte_unstuff(self):
        stuffed = bytearray([
            JPCProtocol.FRAME_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            JPCProtocol.FRAME_BYTE ^ JPCProtocol.XOR_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            JPCProtocol.ESCAPE_BYTE ^ JPCProtocol.XOR_BYTE,
            0xFF,
            JPCProtocol.FRAME_BYTE
        ])

        unstuffed = bytearray([
            0xFF,
            JPCProtocol.FRAME_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            0xFF
        ])

        expected = [unstuffed]
        actual = byte_unstuff(stuffed)
        self.assertEqual(expected, actual)

    def test_append_and_remove_crc(self):
        stuffed = bytearray([
            JPCProtocol.FRAME_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            JPCProtocol.FRAME_BYTE ^ JPCProtocol.XOR_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            JPCProtocol.ESCAPE_BYTE ^ JPCProtocol.XOR_BYTE,
            0xFF,
            JPCProtocol.FRAME_BYTE
        ])

        unstuffed = bytearray([
            0xFF,
            JPCProtocol.FRAME_BYTE,
            0xFF,
            JPCProtocol.ESCAPE_BYTE,
            0xFF
        ])

        unstuffed, crc = append_crc(unstuffed)
        stuffed = byte_stuff(unstuffed)
        unstuffed = byte_unstuff(stuffed)
        unstuffed, crc2 = remove_crc(unstuffed[0])
        self.assertEqual(crc, crc2)



if __name__ == '__main__':
    unittest.main()
