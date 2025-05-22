from src.models.user import User

class UserRepository:
    def __init__(self, mongo_db):
        self.collection = mongo_db["users"]

    def add_user(self, user: User):
        # Verifica si el usuario ya existe antes de insertar
        if self.username_exists(user.username):
            return False
        try:
            self.collection.insert_one({
                "username": user.username,
                "password_hash": user.password_hash,
                "tokens": [str(t) for t in user.tokens]
            })
            return True
        except Exception as e:
            # Puedes loggear el error si lo deseas
            return False

    def get_user(self, username: str):
        doc = self.collection.find_one({"username": username})
        if doc:
            user = User(doc["username"], doc["password_hash"])
            user.tokens = [str(t) for t in doc.get("tokens", [])]
            return user
        return None

    def username_exists(self, username: str) -> bool:
        return self.collection.count_documents({"username": username}) > 0

    def update_user_tokens(self, username: str, tokens: list):
        self.collection.update_one({"username": username}, {"$set": {"tokens": [str(t) for t in tokens]}})
