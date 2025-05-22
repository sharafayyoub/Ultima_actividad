import gradio as gr
from src.services.chatbot_service import ChatbotService

def build_gradio_ui(poll_service, nft_service=None, user_service=None):
    chatbot_service = ChatbotService(poll_service)

    def register(username, password):
        try:
            user_service.register(username, password)
            return "Registro exitoso. Ahora puedes iniciar sesión."
        except ValueError as e:
            return f"Error: {e}"

    def login(username, password):
        token = user_service.login(username, password)
        if token:
            return f"Login exitoso. Bienvenido, {username}.", username
        else:
            return "Credenciales incorrectas.", None

    def chatbot_response_fn(message, username="anon"):
        return chatbot_service.chatbot_response(message, username)

    def tokens_table(username="anon"):
        if nft_service and username:
            tokens = nft_service.get_tokens_by_owner(username)
            rows = [[t.token_id, t.poll_id, t.option, t.issued_at.strftime("%Y-%m-%d %H:%M:%S")] for t in tokens]
            return rows
        return []

    def create_poll_ui(pregunta, opciones, duracion, tipo):
        try:
            opciones_list = [o.strip() for o in opciones.split(",") if o.strip()]
            poll_id = poll_service.create_poll(pregunta, opciones_list, int(duracion), tipo)
            return f"Encuesta creada con ID: {poll_id}"
        except Exception as e:
            return f"Error: {e}"

    def list_polls_ui():
        polls = poll_service.poll_repo.all_polls()
        rows = []
        for p in polls:
            rows.append([
                p.id, p.pregunta, ", ".join(p.opciones), p.estado, p.tipo, p.timestamp_inicio.strftime("%Y-%m-%d %H:%M:%S")
            ])
        return rows

    def vote_ui(poll_id, username, opcion):
        try:
            poll = poll_service.poll_repo.get_poll(poll_id)
            if not poll:
                return "Encuesta no encontrada."
            if poll.tipo == "simple":
                poll_service.vote(poll_id, username, opcion)
            else:
                opciones = [o.strip() for o in opcion.split(",") if o.strip()]
                poll_service.vote(poll_id, username, opciones)
            return "Voto registrado correctamente."
        except Exception as e:
            return f"Error: {e}"

    def close_poll_ui(poll_id):
        try:
            poll_service.close_poll(poll_id)
            return "Encuesta cerrada."
        except Exception as e:
            return f"Error: {e}"

    def partial_results_ui(poll_id):
        try:
            res = poll_service.get_partial_results(poll_id)
            return str(res)
        except Exception as e:
            return f"Error: {e}"

    def final_results_ui(poll_id):
        try:
            res = poll_service.get_final_results(poll_id)
            return str(res)
        except Exception as e:
            return f"Error: {e}"

    with gr.Blocks() as demo:
        gr.Markdown("# Encuestas Interactivas")

        with gr.Tab("Login / Registro"):
            gr.Markdown("## Registro")
            reg_user = gr.Textbox(label="Usuario")
            reg_pass = gr.Textbox(label="Contraseña", type="password")
            reg_btn = gr.Button("Registrarse")
            reg_out = gr.Textbox(label="Resultado registro")
            reg_btn.click(register, inputs=[reg_user, reg_pass], outputs=reg_out)

            gr.Markdown("## Login")
            login_user = gr.Textbox(label="Usuario")
            login_pass = gr.Textbox(label="Contraseña", type="password")
            login_btn = gr.Button("Iniciar sesión")
            login_out = gr.Textbox(label="Resultado login")
            logged_user = gr.State()
            login_btn.click(login, inputs=[login_user, login_pass], outputs=[login_out, logged_user])

        with gr.Tab("Encuestas"):
            gr.Markdown("## Crear Encuesta")
            pregunta = gr.Textbox(label="Pregunta")
            opciones = gr.Textbox(label="Opciones (separadas por coma)")
            duracion = gr.Number(label="Duración (segundos)", value=60)
            tipo = gr.Dropdown(choices=["simple", "multiple"], label="Tipo", value="simple")
            crear_btn = gr.Button("Crear Encuesta")
            crear_out = gr.Textbox(label="Resultado creación")
            crear_btn.click(create_poll_ui, inputs=[pregunta, opciones, duracion, tipo], outputs=crear_out)

            gr.Markdown("## Listar Encuestas")
            polls_df = gr.Dataframe(headers=["ID", "Pregunta", "Opciones", "Estado", "Tipo", "Inicio"])
            list_btn = gr.Button("Actualizar lista")
            list_btn.click(list_polls_ui, outputs=polls_df)

            gr.Markdown("## Votar en Encuesta")
            poll_id_vote = gr.Textbox(label="ID Encuesta")
            username_vote = gr.Textbox(label="Usuario")
            opcion_vote = gr.Textbox(label="Opción (o lista separada por coma si es múltiple)")
            vote_btn = gr.Button("Votar")
            vote_out = gr.Textbox(label="Resultado voto")
            vote_btn.click(vote_ui, inputs=[poll_id_vote, username_vote, opcion_vote], outputs=vote_out)

            gr.Markdown("## Cerrar Encuesta Manualmente")
            poll_id_close = gr.Textbox(label="ID Encuesta a cerrar")
            close_btn = gr.Button("Cerrar Encuesta")
            close_out = gr.Textbox(label="Resultado cierre")
            close_btn.click(close_poll_ui, inputs=poll_id_close, outputs=close_out)

            gr.Markdown("## Resultados Parciales")
            poll_id_partial = gr.Textbox(label="ID Encuesta")
            partial_btn = gr.Button("Ver Parciales")
            partial_out = gr.Textbox(label="Parciales")
            partial_btn.click(partial_results_ui, inputs=poll_id_partial, outputs=partial_out)

            gr.Markdown("## Resultados Finales")
            poll_id_final = gr.Textbox(label="ID Encuesta")
            final_btn = gr.Button("Ver Finales")
            final_out = gr.Textbox(label="Finales")
            final_btn.click(final_results_ui, inputs=poll_id_final, outputs=final_out)

        with gr.Tab("Encuestas y Chatbot"):
            gr.Markdown("**Primero inicia sesión en la pestaña anterior. Luego escribe tu usuario aquí:**")
            user_input = gr.Textbox(label="Usuario autenticado")
            chat_history = gr.Chatbot(label="Chat")
            chat_msg = gr.Textbox(label="Mensaje")
            send_btn = gr.Button("Enviar mensaje")

            def chat_interact(history, msg, username):
                if not username:
                    return history + [[msg, "Por favor, inicia sesión primero."]], ""
                response = chatbot_response_fn(msg, username)
                return history + [[msg, response]], ""

            send_btn.click(
                chat_interact,
                inputs=[chat_history, chat_msg, user_input],
                outputs=[chat_history, chat_msg]
            )

            gr.Markdown("## Mis Tokens NFT")
            tokens_df = gr.Dataframe(headers=["Token ID", "Poll ID", "Opción", "Emitido"])
            show_tokens_btn = gr.Button("Mostrar mis tokens")
            show_tokens_btn.click(
                lambda username: tokens_table(username),
                inputs=[user_input],
                outputs=[tokens_df]
            )

            gr.Markdown("## Transferir (Tradear) Token NFT")
            trade_token_id = gr.Textbox(label="Token ID a transferir")
            trade_new_owner = gr.Textbox(label="Nuevo propietario (usuario destino)")
            trade_current_owner = gr.Textbox(label="Tu usuario (debe ser el propietario)")
            trade_btn = gr.Button("Transferir Token")
            trade_out = gr.Textbox(label="Resultado transferencia")

            def transfer_token_ui(token_id, current_owner, new_owner):
                if not nft_service:
                    return "Servicio NFT no disponible."
                try:
                    nft_service.transfer_token(token_id, current_owner, new_owner)
                    return f"Token {token_id} transferido a {new_owner}."
                except Exception as e:
                    return f"Error: {e}"

            trade_btn.click(
                transfer_token_ui,
                inputs=[trade_token_id, trade_current_owner, trade_new_owner],
                outputs=trade_out
            )

    return demo
