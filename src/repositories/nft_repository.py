from src.models.token_nft import TokenNFT
from datetime import datetime

class NFTRepository:
    def __init__(self, mongo_db):
        self.collection = mongo_db["tokens"]

    def add_token(self, token: TokenNFT):
        self.collection.insert_one({
            "token_id": token.token_id,
            "owner": token.owner,
            "poll_id": token.poll_id,
            "option": token.option,
            "issued_at": token.issued_at.isoformat()
        })

    def get_token(self, token_id: str):
        doc = self.collection.find_one({"token_id": token_id})
        if doc:
            token = TokenNFT(doc["owner"], doc["poll_id"], doc["option"])
            token.token_id = doc["token_id"]
            token.issued_at = datetime.fromisoformat(doc["issued_at"])
            return token
        return None

    def get_tokens_by_owner(self, owner: str):
        docs = self.collection.find({"owner": owner})
        tokens = []
        for doc in docs:
            token = TokenNFT(doc["owner"], doc["poll_id"], doc["option"])
            token.token_id = doc["token_id"]
            token.issued_at = datetime.fromisoformat(doc["issued_at"])
            tokens.append(token)
        return tokens

    def transfer_token(self, token_id: str, new_owner: str):
        result = self.collection.update_one({"token_id": token_id}, {"$set": {"owner": new_owner}})
        return result.modified_count > 0

    def all_tokens(self):
        docs = self.collection.find()
        tokens = []
        for doc in docs:
            token = TokenNFT(doc["owner"], doc["poll_id"], doc["option"])
            token.token_id = doc["token_id"]
            token.issued_at = datetime.fromisoformat(doc["issued_at"])
            tokens.append(token)
        return tokens
