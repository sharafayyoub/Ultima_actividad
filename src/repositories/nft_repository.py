from src.models.token_nft import TokenNFT

class NFTRepository:
    def __init__(self):
        self.tokens = {}  # token_id -> TokenNFT

    def add_token(self, token: TokenNFT):
        self.tokens[token.token_id] = token

    def get_token(self, token_id: str):
        return self.tokens.get(token_id)

    def get_tokens_by_owner(self, owner: str):
        return [t for t in self.tokens.values() if t.owner == owner]

    def transfer_token(self, token_id: str, new_owner: str):
        token = self.get_token(token_id)
        if token:
            token.owner = new_owner
            return True
        return False

    def all_tokens(self):
        return list(self.tokens.values())
