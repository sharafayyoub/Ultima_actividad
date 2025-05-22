from pymongo import MongoClient, errors
from src.repositories.user_repository import UserRepository
from src.repositories.poll_repository import PollRepository
from src.repositories.nft_repository import NFTRepository
from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService
from src.ui.gradio_ui import build_gradio_ui
import gradio as gr

def build_error_ui(msg):
    with gr.Blocks() as demo:
        gr.Markdown(f"## ❌ {msg}")
        gr.Markdown("Asegúrate de que el servicio de MongoDB está corriendo en localhost:27017 antes de iniciar la app.")
    return demo

def main():
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        client.server_info()  # Fuerza la conexión para detectar errores rápido
        mongo_db = client["streaming_app"]
    except errors.ServerSelectionTimeoutError:
        demo = build_error_ui("No se pudo conectar a MongoDB.")
        demo.launch(share=True)
        return

    # Inicialización de repositorios y servicios con MongoDB
    user_repo = UserRepository(mongo_db)
    poll_repo = PollRepository(mongo_db)
    nft_repo = NFTRepository(mongo_db)

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
