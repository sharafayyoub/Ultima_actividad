from src.repositories.nft_repository import NFTRepository
from src.models.token_nft import TokenNFT

class NFTService:
    def __init__(self, nft_repo: NFTRepository):
        self.nft_repo = nft_repo

    def mint_token(self, owner: str, poll_id: str, option: str):
        token = TokenNFT(owner, poll_id, option)
        self.nft_repo.add_token(token)
        return token

    def transfer_token(self, token_id: str, current_owner: str, new_owner: str):
        token = self.nft_repo.get_token(token_id)
        if not token or token.owner != current_owner:
            raise ValueError("No tienes permiso para transferir este token.")
        self.nft_repo.transfer_token(token_id, new_owner)
        return True

    def get_tokens_by_owner(self, owner: str):
        return self.nft_repo.get_tokens_by_owner(owner)
