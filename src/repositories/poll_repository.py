from src.models.poll import Poll

class PollRepository:
    def __init__(self):
        self.polls = {}  # poll_id -> Poll

    def add_poll(self, poll: Poll):
        self.polls[poll.id] = poll

    def get_poll(self, poll_id: str):
        return self.polls.get(poll_id)

    def get_active_polls(self):
        return [p for p in self.polls.values() if p.estado == "activa"]

    def all_polls(self):
        return list(self.polls.values())
