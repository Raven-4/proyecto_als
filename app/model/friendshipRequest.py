import sirope

class FriendshipRequest:
    def __init__(self, id, sender, receiver):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.status = "pending"  # Por defecto, la solicitud está pendiente de aceptación
    
    @property
    def id(self):
        return self._id
    
    @property
    def sender(self):
        return self._sender
    
    @property
    def receiver(self):
        return self._receiver

    def accept(self):
        self.status = "accepted"

    def reject(self):
        self.status = "rejected"
