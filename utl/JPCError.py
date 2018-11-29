class JPCHeartbeatTimeout(Exception):
    def __init__(self, user):
        self.user = user
