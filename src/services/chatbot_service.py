# ...existing imports...
import re

class ChatbotService:
    def __init__(self, poll_service):
        self.poll_service = poll_service
        self.histories = {}  # username -> list of (user_msg, bot_msg)

    def chatbot_response(self, message, username=None):
        # Palabras clave para respuestas contextuales
        msg = message.lower()
        if any(kw in msg for kw in ["quién va ganando", "quien va ganando", "quién lidera", "quien lidera"]):
            # Consulta resultados parciales
            poll = self.poll_service.get_active_poll()
            if poll:
                results = self.poll_service.get_partial_results(poll.id)
                winner = max(results, key=results.get)
                response = f"La opción que va ganando es '{winner}' con {results[winner]} votos."
            else:
                response = "No hay encuestas activas en este momento."
        elif any(kw in msg for kw in ["cuánto falta", "cuanto falta", "tiempo restante"]):
            poll = self.poll_service.get_active_poll()
            if poll:
                seconds_left = self.poll_service.get_time_left(poll.id)
                response = f"Quedan {seconds_left} segundos para que termine la encuesta."
            else:
                response = "No hay encuestas activas en este momento."
        else:
            # Respuesta genérica simulada
            response = "¡Gracias por tu mensaje! Pregúntame sobre las encuestas o cualquier otra cosa."
        # Guardar historial (opcional)
        if username:
            self.histories.setdefault(username, []).append((message, response))
        return response
