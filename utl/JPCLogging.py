class JPCLogger:
    def log_rx(packet, t):
        length = len(str(packet))
        print('{};{};{};{};'.format(t, 'rx', length, packet))
        print(length)

    def log_tx(packet, t):
        length = len(str(packet))
        print('{};{};{};{};'.format(t, 'tx', length, packet))
        print(length)
