from src.models.poll import Poll
from datetime import datetime

class PollRepository:
    def __init__(self, mongo_db):
        self.collection = mongo_db["polls"]

    def add_poll(self, poll: Poll):
        self.collection.insert_one({
            "id": poll.id,
            "pregunta": poll.pregunta,
            "opciones": poll.opciones,
            "duracion_segundos": poll.duracion_segundos,
            "tipo": poll.tipo,
            "timestamp_inicio": poll.timestamp_inicio.isoformat(),
            "estado": poll.estado,
            "votos": poll.votos,
            "resultado": poll.resultado
        })

    def get_poll(self, poll_id: str):
        doc = self.collection.find_one({"id": poll_id})
        if doc:
            poll = Poll(
                doc["pregunta"],
                doc["opciones"],
                doc["duracion_segundos"],
                doc["tipo"]
            )
            poll.id = doc["id"]
            poll.timestamp_inicio = datetime.fromisoformat(doc["timestamp_inicio"])
            poll.estado = doc["estado"]
            poll.votos = doc.get("votos", {})
            poll.resultado = doc.get("resultado")
            return poll
        return None

    def get_active_polls(self):
        docs = self.collection.find({"estado": "activa"})
        return [self.get_poll(doc["id"]) for doc in docs]

    def all_polls(self):
        docs = self.collection.find()
        return [self.get_poll(doc["id"]) for doc in docs]

    def update_poll(self, poll: Poll):
        self.collection.update_one(
            {"id": poll.id},
            {"$set": {
                "estado": poll.estado,
                "votos": poll.votos,
                "resultado": poll.resultado
            }}
        )
