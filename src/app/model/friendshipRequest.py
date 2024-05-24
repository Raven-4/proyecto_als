import sirope

class FriendshipRequest:
    def __init__(self, id, sender, receiver, status):
        self._id = id
        self._sender = sender
        self._receiver = receiver
        self._status = status 
    
    @property
    def id(self):
        return self._id
    
    @property
    def sender(self):
        return self._sender
    
    @property
    def receiver(self):
        return self._receiver

    @property
    def status(self):
        return self._status
    
    def accept(self):
        self._status = "accepted"

    def reject(self):
        self._status = "rejected"

    def delete_request(self):
        sirope.Sirope.delete(self)

