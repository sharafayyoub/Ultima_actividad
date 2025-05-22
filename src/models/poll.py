import uuid
from datetime import datetime

class Poll:
    def __init__(self, pregunta, opciones, duracion_segundos, tipo):
        self.id = str(uuid.uuid4())
        self.pregunta = pregunta
        self.opciones = opciones  # List[str]
        self.duracion_segundos = duracion_segundos
        self.tipo = tipo  # "simple" o "multiple"
        self.timestamp_inicio = datetime.now()
        self.estado = "activa"  # o "cerrada"
        self.votos = {}  # username -> opcion (o lista de opciones)
        self.resultado = None  # Se llena al cerrar

    def esta_activa(self):
        from datetime import datetime, timedelta
        if self.estado != "activa":
            return False
        fin = self.timestamp_inicio + timedelta(seconds=self.duracion_segundos)
        return datetime.now() < fin
