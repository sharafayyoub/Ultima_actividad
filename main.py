from pymongo import MongoClient, errors
from src.repositories.user_repository import UserRepository
from src.repositories.poll_repository import PollRepository
from src.repositories.nft_repository import NFTRepository
from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService
from src.ui.gradio_ui import build_gradio_ui
import gradio as gr

# Fallback repositorios en memoria
class InMemoryUserRepository:
    def __init__(self, _=None):
        self.users = {}
    def add_user(self, user): self.users[user.username] = user; return True
    def get_user(self, username): return self.users.get(username)
    def username_exists(self, username): return username in self.users
    def update_user_tokens(self, username, tokens): 
        if username in self.users: self.users[username].tokens = tokens

class InMemoryPollRepository:
    def __init__(self, _=None):
        self.polls = {}
    def add_poll(self, poll): self.polls[poll.id] = poll
    def get_poll(self, poll_id): return self.polls.get(poll_id)
    def get_active_polls(self): return [p for p in self.polls.values() if p.estado == "activa"]
    def all_polls(self): return list(self.polls.values())
    def update_poll(self, poll): self.polls[poll.id] = poll

class InMemoryNFTRepository:
    def __init__(self, _=None):
        self.tokens = {}
    def add_token(self, token): self.tokens[token.token_id] = token
    def get_token(self, token_id): return self.tokens.get(token_id)
    def get_tokens_by_owner(self, owner): return [t for t in self.tokens.values() if t.owner == owner]
    def transfer_token(self, token_id, new_owner):
        token = self.get_token(token_id)
        if token: token.owner = new_owner; return True
        return False
    def all_tokens(self): return list(self.tokens.values())

def build_error_ui(msg):
    with gr.Blocks() as demo:
        gr.Markdown(f"## ❌ {msg}")
        gr.Markdown("Asegúrate de que el servicio de MongoDB está corriendo en localhost:27017 antes de iniciar la app.")
        gr.Markdown("Se usará almacenamiento en memoria (los datos NO se guardarán tras cerrar la app).")
    return demo

def main():
    mongo_ok = True
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        client.server_info()
        mongo_db = client["streaming_app"]
    except errors.ServerSelectionTimeoutError:
        mongo_ok = False
        demo = build_error_ui("No se pudo conectar a MongoDB.")
        print("No se pudo conectar a MongoDB. Usando almacenamiento en memoria.")
        mongo_db = None

    # Usa repositorios MongoDB si está disponible, si no, usa en memoria
    user_repo = UserRepository(mongo_db) if mongo_ok else InMemoryUserRepository()
    poll_repo = PollRepository(mongo_db) if mongo_ok else InMemoryPollRepository()
    nft_repo = NFTRepository(mongo_db) if mongo_ok else InMemoryNFTRepository()

    user_service = UserService(user_repo)
    nft_service = NFTService(nft_repo)
    poll_service = PollService(poll_repo, nft_service)

    demo = build_gradio_ui(
        poll_service=poll_service,
        nft_service=nft_service,
        user_service=user_service
    )
    demo.launch(share=True)

if __name__ == "__main__":
    main()
