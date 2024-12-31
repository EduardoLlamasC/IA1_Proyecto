from tkinter import Tk, Label, Text, Scrollbar, Entry, Button, Frame
from tkinter import DISABLED, END, NORMAL
from chat import get_prediction

# Nuevos colores y estilo minimalista
BG_COLOR = "#E9ECEF"  # Fondo claro para un aspecto más limpio
TEXT_COLOR = "#495057"  # Texto oscuro
USER_COLOR = "#007BFF"  # Azul para los mensajes del usuario
BOT_COLOR = "#28A745"  # Verde para los mensajes del bot
FONT = "Helvetica 12"
FONT_BOLD = "Helvetica 14 bold"

class App:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=500, height=650, background=BG_COLOR)

        # Creación de un marco para organizar mejor los elementos
        main_frame = Frame(self.window, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        head_label = Label(
            main_frame, 
            bg=BG_COLOR, 
            fg=TEXT_COLOR, 
            text="Chatbot", 
            font=FONT_BOLD, 
            pady=10
        )
        head_label.pack()

        # Área de chat con borde redondeado y sombra
        self.text_widget = Text(
            main_frame,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=FONT,
            wrap="word",
            height=20,
            padx=10,
            pady=10,
            bd=0,
            state=DISABLED,
            relief="flat"
        )
        self.text_widget.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.98)
        scrollbar.configure(command=self.text_widget.yview)

        # Entrada de texto con borde redondeado
        self.msg_entry = Entry(
            main_frame, 
            bg="#FFFFFF", 
            fg=TEXT_COLOR, 
            font=FONT, 
            bd=2, 
            relief="solid", 
            justify="left"
        )
        self.msg_entry.pack(padx=10, pady=(10, 20), fill="x")
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # Botón de envío con un diseño moderno (bordes redondeados, color llamativo)
        send_button = Button(
            main_frame,
            text="Enviar",
            font=FONT_BOLD,
            bg=USER_COLOR,
            fg="white",
            relief="flat",
            command=lambda: self._on_enter_pressed(None),
            width=20
        )
        send_button.pack(pady=10)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "Tú")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        # Insertar el mensaje del usuario con formato
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg} \n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        # Respuesta del bot con color diferente
        bot_reply = get_prediction(msg)
        msg2 = f"Chatbot: {bot_reply} \n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        # Desplazar la vista hacia el último mensaje
        self.text_widget.see(END)

if __name__ == '__main__':
    app = App()
    app.run()
