class JPCProtocol:
    # opcodes
    HELLO = 0
    CLOSE = 1
    HEARTBEAT = 2
    ERROR = 3
    SEND = 4
    TELL = 5

    # error codes
    ERROR_UNKNOWN = 0
    ERROR_TIMED_OUT = 1

    # misc
    HEARTBEAT_INTERVAL = 3
    HEARTBEAT_TIMEOUT = 10
    STANDARD_PORT = 27272

    # byte stuffing
    FRAME_BYTE = 0x7E
    ESCAPE_BYTE = 0x7D
    XOR_BYTE = 0x20

    # message types
    MESSAGE_TEXT = 0
    MESSAGE_IMG = 1
