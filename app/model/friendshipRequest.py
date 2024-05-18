class FriendshipRequest:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver
        self.status = "pending"  # Por defecto, la solicitud está pendiente de aceptación

    def accept(self):
        self.status = "accepted"

    def reject(self):
        self.status = "rejected"
