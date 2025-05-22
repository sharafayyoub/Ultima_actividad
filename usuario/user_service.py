import hashlib
import os
import uuid

class User:
    def __init__(self, username: str, password_hash: bytes, salt: bytes):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt

class UserService:
    def __init__(self):
        # Almacén de usuarios registrados
        self.users = {}
        # Almacén de sesiones activas: {token_uuid: username}
        self.active_sessions = {}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            print("Error: El nombre de usuario ya existe.")
            return False

        salt = os.urandom(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), salt, 100000
        )

        user = User(username, password_hash, salt)
        self.users[username] = user
        print(f"Usuario '{username}' registrado con éxito.")
        return True

    def authenticate(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if not user:
            return False

        input_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), user.salt, 100000
        )

        return input_hash == user.password_hash

    def login(self, username: str, password: str) -> str | None:
        if not self.authenticate(username, password):
            print("Error: Credenciales inválidas.")
            return None

        session_token = str(uuid.uuid4())
        self.active_sessions[session_token] = username
        print(f"Usuario '{username}' ha iniciado sesión. Token: {session_token}")
        return session_token

    def get_logged_in_user(self, token: str) -> str | None:
        return self.active_sessions.get(token)


