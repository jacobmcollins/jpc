class JPCLogger:
    @staticmethod
    def log_rx(packet, t):
        length = len(str(packet))
        print('{};{};{};{};'.format(t, 'rx', length, packet))

    @staticmethod
    def log_tx(packet, t):
        length = len(str(packet))
        print('{};{};{};{};'.format(t, 'tx', length, packet))
