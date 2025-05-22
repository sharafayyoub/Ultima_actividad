from src.models.user import User

class UserRepository:
    def __init__(self):
        self.users = {}  # username -> User

    def add_user(self, user: User):
        self.users[user.username] = user

    def get_user(self, username: str):
        return self.users.get(username)

    def username_exists(self, username: str) -> bool:
        return username in self.users
