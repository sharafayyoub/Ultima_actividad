import hashlib
import uuid
from src.repositories.user_repository import UserRepository
from src.models.user import User

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.sessions = {}  # session_token -> username

    def hash_password(self, password: str, salt: bytes = None):
        if not salt:
            salt = uuid.uuid4().bytes
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt.hex() + ':' + pwd_hash.hex()

    def verify_password(self, password: str, stored_hash: str):
        salt_hex, pwd_hash_hex = stored_hash.split(':')
        salt = bytes.fromhex(salt_hex)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return pwd_hash.hex() == pwd_hash_hex

    def register(self, username: str, password: str):
        if self.user_repo.username_exists(username):
            raise ValueError("Username already exists")
        password_hash = self.hash_password(password)
        user = User(username, password_hash)
        self.user_repo.add_user(user)
        return True

    def login(self, username: str, password: str):
        user = self.user_repo.get_user(username)
        if not user or not self.verify_password(password, user.password_hash):
            return None
        session_token = str(uuid.uuid4())
        self.sessions[session_token] = username
        return session_token

    def get_username_by_token(self, session_token: str):
        return self.sessions.get(session_token)
