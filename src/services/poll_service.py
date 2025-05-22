from datetime import datetime
from src.repositories.poll_repository import PollRepository
from src.models.poll import Poll
from src.services.nft_service import NFTService

class PollService:
    def __init__(self, poll_repo: PollRepository, nft_service: NFTService):
        self.poll_repo = poll_repo
        self.nft_service = nft_service

    def create_poll(self, pregunta, opciones, duracion_segundos, tipo):
        poll = Poll(pregunta, opciones, duracion_segundos, tipo)
        self.poll_repo.add_poll(poll)
        return poll.id

    def vote(self, poll_id, username, opcion):
        poll = self.poll_repo.get_poll(poll_id)
        self._auto_close_expired_polls()
        if not poll or poll.estado != "activa":
            raise ValueError("Encuesta no activa")
        if username in poll.votos:
            raise ValueError("Usuario ya votó")
        # Validación de opción
        if poll.tipo == "simple":
            if opcion not in poll.opciones:
                raise ValueError("Opción inválida")
            poll.votos[username] = opcion
        else:  # multiple
            if not isinstance(opcion, list) or not all(o in poll.opciones for o in opcion):
                raise ValueError("Opciones inválidas")
            poll.votos[username] = opcion
        self.nft_service.mint_token(username, poll_id, opcion)
        # Persistir cambios en la encuesta
        self.poll_repo.update_poll(poll)
        return True

    def close_poll(self, poll_id):
        poll = self.poll_repo.get_poll(poll_id)
        if poll and poll.estado == "activa":
            poll.estado = "cerrada"
            poll.resultado = self.get_final_results(poll_id)
            # Persistir cambios en la encuesta
            self.poll_repo.update_poll(poll)
            # Notificar observadores aquí si es necesario

    def _auto_close_expired_polls(self):
        for poll in self.poll_repo.get_active_polls():
            if not poll.esta_activa():
                self.close_poll(poll.id)

    def get_partial_results(self, poll_id):
        poll = self.poll_repo.get_poll(poll_id)
        if not poll:
            return {}
        total = len(poll.votos)
        conteo = {}
        for v in poll.votos.values():
            if isinstance(v, list):
                for o in v:
                    conteo[o] = conteo.get(o, 0) + 1
            else:
                conteo[v] = conteo.get(v, 0) + 1
        porcentajes = {k: (v / total * 100 if total > 0 else 0) for k, v in conteo.items()}
        return {"conteo": conteo, "porcentajes": porcentajes}

    def get_final_results(self, poll_id):
        poll = self.poll_repo.get_poll(poll_id)
        if not poll or poll.estado != "cerrada":
            return {}
        return self.get_partial_results(poll_id)

    def get_active_poll(self):
        activos = self.poll_repo.get_active_polls()
        return activos[0] if activos else None

    def get_time_left(self, poll_id):
        poll = self.poll_repo.get_poll(poll_id)
        if not poll or poll.estado != "activa":
            return 0
        from datetime import datetime
        fin = poll.timestamp_inicio.timestamp() + poll.duracion_segundos
        restante = fin - datetime.now().timestamp()
        return max(0, int(restante))
