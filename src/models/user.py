import uuid

class User:
    def __init__(self, username: str, password_hash: str):
        self.username = username
        self.password_hash = password_hash
        self.tokens = []  # Lista de TokenNFT ids

    def add_token(self, token_id: str):
        self.tokens.append(token_id)
