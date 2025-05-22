from src.repositories.user_repository import UserRepository
from src.repositories.poll_repository import PollRepository
from src.repositories.nft_repository import NFTRepository
from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService
from src.ui.gradio_ui import build_gradio_ui

def main():
    # Inicialización de repositorios y servicios
    user_repo = UserRepository()
    poll_repo = PollRepository()
    nft_repo = NFTRepository()

    user_service = UserService(user_repo)
    nft_service = NFTService(nft_repo)
    poll_service = PollService(poll_repo, nft_service)

    # Ejecuta directamente la interfaz Gradio con todos los servicios
    demo = build_gradio_ui(
        poll_service=poll_service,
        nft_service=nft_service,
        user_service=user_service
    )
    demo.launch(share=True)

if __name__ == "__main__":
    main()
