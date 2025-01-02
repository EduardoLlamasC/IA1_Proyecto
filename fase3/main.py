from tkinter import Tk, Label, Text, Scrollbar, Entry, Button, Frame, Canvas
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
        self.window.title("Proyecto IA1 - Fase 3")
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

        # Scrollbar para el área de texto
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

        # Cuadro de preguntas sugeridas con scroll
        self.suggested_questions_frame = Frame(main_frame, bg=BG_COLOR)
        self.suggested_questions_frame.pack(padx=10, pady=(10, 20), fill="x")

        # Canvas para permitir el scroll de las preguntas
        canvas = Canvas(self.suggested_questions_frame, bg=BG_COLOR)
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar para las preguntas sugeridas
        scrollbar_suggestions = Scrollbar(self.suggested_questions_frame, orient="vertical", command=canvas.yview)
        scrollbar_suggestions.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar_suggestions.set)

        # Frame dentro del canvas para contener los botones
        self.questions_frame = Frame(canvas, bg=BG_COLOR)
        canvas.create_window((0, 0), window=self.questions_frame, anchor="nw")

        # Lista de preguntas sugeridas
        suggested_questions = [
            "Hi", "How are you", "Is anyone there?", "Hello", "Good day", "Hey", "What's up?", "How's it going?", "Hola", "Good morning", "Hello there", "Bye", "See you later", "Goodbye", "Take care", "See you soon", "Farewell", "Good night", "Catch you later", "Thanks", "Thank you", "That's helpful", "Thanks a lot", "Thank you very much", "I appreciate it", "Thanks for the help", "Thanks for your assistance", "How to sum two numbers in Python?", "Write a Python program to add two numbers", "Python sum example", "Show me how to add two numbers in Python", "Give me the code for adding two numbers in Python", "Can you write a Python code to sum two numbers?", "Python sum function", "Add numbers in Python", "Sum of two numbers in Python", "How to sum two numbers in JavaScript?", "Write a JavaScript program to add two numbers", "JavaScript sum example", "Show me how to add two numbers in JavaScript", "Give me the code for adding two numbers in JavaScript", "Can you write a JavaScript code to sum two numbers?", "JavaScript sum function", "Add numbers in JavaScript", "Sum of two numbers in JavaScript", "How to find factorial in Python?", "Write a Python program to calculate factorial", "Python factorial example", "How can I calculate the factorial of a number in Python?", "Give me a Python code for factorial", "Can you show me Python code for calculating factorial?", "Factorial function in Python", "How to calculate factorial using Python?", "How to find factorial in JavaScript?", "Write a JavaScript program to calculate factorial", "JavaScript factorial example", "How can I calculate the factorial of a number in JavaScript?", "Give me a JavaScript code for factorial", "Can you show me JavaScript code for calculating factorial?", "Factorial function in JavaScript", "How to calculate factorial using JavaScript?", "How to generate Fibonacci sequence in Python?", "Write a Python program to generate Fibonacci sequence", "Python Fibonacci example", "How can I generate Fibonacci series in Python?", "Give me the Python code for Fibonacci sequence", "Can you show me the Python code for Fibonacci numbers?", "Fibonacci series in Python", "How to write Fibonacci sequence function in Python?", "How to generate Fibonacci sequence in JavaScript?", "Write a JavaScript program to generate Fibonacci sequence", "JavaScript Fibonacci example", "How can I generate Fibonacci series in JavaScript?", "Give me the JavaScript code for Fibonacci sequence", "Can you show me the JavaScript code for Fibonacci numbers?", "Fibonacci series in JavaScript", "How to write Fibonacci sequence function in JavaScript?", "How to reverse a string in Python?", "Write a Python program to reverse a string", "Python reverse string example", "How can I reverse a string in Python?", "Give me the Python code to reverse a string", "Can you show me Python code for reversing a string?", "Reverse a string in Python", "How to reverse a string in JavaScript?", "Write a JavaScript program to reverse a string", "JavaScript reverse string example", "How can I reverse a string in JavaScript?", "Give me the JavaScript code to reverse a string", "Can you show me JavaScript code for reversing a string?", "Reverse a string in JavaScript",
            "How to check if a string is a palindrome in Python?", "Write a Python program to check palindrome", "Python palindrome example", "How can I check if a word is a palindrome in Python?", "Give me the Python code to check palindrome", "Can you show me Python code for palindrome check?", "Palindrome function in Python", "Check if a string is palindrome in Python", "How to check if a string is a palindrome in JavaScript?", "Write a JavaScript program to check palindrome", "JavaScript palindrome example", "How can I check if a word is a palindrome in JavaScript?", "Give me the JavaScript code to check palindrome", "Can you show me JavaScript code for palindrome check?", "Palindrome function in JavaScript", "Check if a string is palindrome in JavaScript", "How to find the maximum number in a list in Python?", "Write a Python program to find the largest number in a list", "Python max number example", "How can I find the maximum number in a list in Python?", "Give me the Python code to find the maximum number", "Can you show me Python code for finding the maximum number?", "Find the largest number in Python", "Max number in Python", "How to find the maximum number in an array in JavaScript?", "Write a JavaScript program to find the largest number in an array", "JavaScript max number example", "How can I find the maximum number in an array in JavaScript?", "Give me the JavaScript code to find the maximum number", "Can you show me JavaScript code for finding the maximum number?", "Find the largest number in JavaScript", "Max number in JavaScript", "How to swap two numbers in Python?", "Write a Python program to swap two numbers", "Python swap example", "How can I swap two variables in Python?", "Give me the Python code to swap numbers", "Can you show me Python code for swapping two numbers?", "Swap two numbers in Python", "How to swap two numbers in JavaScript?", "Write a JavaScript program to swap two numbers", "JavaScript swap example", "How can I swap two variables in JavaScript?", "Give me the JavaScript code to swap numbers", "Can you show me JavaScript code for swapping two numbers?", "Swap two numbers in JavaScript", "How to find the sum of digits in Python?", "Write a Python program to calculate sum of digits", "Python program for sum of digits", "Calculate sum of digits in Python", "Python code for summing digits of a number", "How to find the sum of digits in JavaScript?", "Write a JavaScript program to calculate sum of digits", "JavaScript program for sum of digits", "Calculate sum of digits in JavaScript", "JavaScript code for summing digits of a number", "How to find the power of a number in Python?", "Write a Python program to calculate power", "Python program to find power of a number", "Calculate power in Python", "Python code for exponentiation", "How to find the power of a number in JavaScript?", "Write a JavaScript program to calculate power", "JavaScript program to find power of a number", "Calculate power in JavaScript", "JavaScript code for exponentiation", "How to find LCM in Python?", "Write a Python program to calculate LCM", "Python program for Least Common Multiple", "Calculate LCM in Python", "Python code for finding LCM", "How to find LCM in JavaScript?", "Write a JavaScript program to calculate LCM", "JavaScript program for Least Common Multiple", "Calculate LCM in JavaScript", "JavaScript code for finding LCM", "How to find GCD in Python?", "Write a Python program to calculate GCD", "Python program for Greatest Common Divisor", "Calculate GCD in Python", "Python code for finding GCD", "How to find GCD in JavaScript?", "Write a JavaScript program to calculate GCD", "JavaScript program for Greatest Common Divisor", "Calculate GCD in JavaScript", "JavaScript code for finding GCD", "How to check if a number is even or odd in Python?", "Write a Python program to check even or odd", "Python program to check even or odd", "Check if a number is even or odd in Python", "How to check if a number is even or odd in JavaScript?", "Write a JavaScript program to check even or odd", "JavaScript program to check even or odd", "Check if a number is even or odd in JavaScript", "How to calculate area of circle in Python?", "Write a Python program to calculate area of circle", "Python program for area of circle", "Calculate area of circle in Python", "How to calculate area of circle in JavaScript?", "Write a JavaScript program to calculate area of circle", "JavaScript program for area of circle", "Calculate area of circle in JavaScript",
            "¿Cómo sumar dos números en JavaScript?", "Escribe un programa en JavaScript para sumar dos números", "Ejemplo de suma en JavaScript", "Muéstrame cómo sumar dos números en JavaScript", "Dame el código para sumar dos números en JavaScript", "¿Puedes escribir un código en JavaScript para sumar dos números?", "Función de suma en JavaScript", "Sumar números en JavaScript", "Suma de dos números en JavaScript", 
"¿Cómo calcular el factorial en Python?", "Escribe un programa en Python para calcular el factorial", "Ejemplo de factorial en Python", "¿Cómo puedo calcular el factorial de un número en Python?", "Dame un código en Python para calcular el factorial", "¿Puedes mostrarme el código en Python para calcular el factorial?", "Función factorial en Python", "¿Cómo calcular el factorial usando Python?", 
"¿Cómo calcular el factorial en JavaScript?", "Escribe un programa en JavaScript para calcular el factorial", "Ejemplo de factorial en JavaScript", "¿Cómo puedo calcular el factorial de un número en JavaScript?", "Dame un código en JavaScript para calcular el factorial", "¿Puedes mostrarme el código en JavaScript para calcular el factorial?", "Función factorial en JavaScript", "¿Cómo calcular el factorial usando JavaScript?", 
"¿Cómo generar la secuencia de Fibonacci en Python?", "Escribe un programa en Python para generar la secuencia de Fibonacci", "Ejemplo de Fibonacci en Python", "¿Cómo puedo generar la serie de Fibonacci en Python?", "Dame el código en Python para la secuencia de Fibonacci", "¿Puedes mostrarme el código en Python para los números de Fibonacci?", "Secuencia de Fibonacci en Python", "¿Cómo escribir una función para la secuencia de Fibonacci en Python?", 
"¿Cómo generar la secuencia de Fibonacci en JavaScript?", "Escribe un programa en JavaScript para generar la secuencia de Fibonacci", "Ejemplo de Fibonacci en JavaScript", "¿Cómo puedo generar la serie de Fibonacci en JavaScript?", "Dame el código en JavaScript para la secuencia de Fibonacci", "¿Puedes mostrarme el código en JavaScript para los números de Fibonacci?", "Secuencia de Fibonacci en JavaScript", "¿Cómo escribir una función para la secuencia de Fibonacci en JavaScript?", 
"¿Cómo revertir una cadena en Python?", "Escribe un programa en Python para revertir una cadena", "Ejemplo de revertir cadena en Python", "¿Cómo puedo revertir una cadena en Python?", "Dame el código en Python para revertir una cadena", "¿Puedes mostrarme el código en Python para revertir una cadena?", "Revertir una cadena en Python"

        ]

        # Crear botones para cada pregunta sugerida
        for question in suggested_questions:
            btn = Button(
                self.questions_frame,
                text=question,
                font=FONT,
                bg="#F1F1F1",
                fg=TEXT_COLOR,
                relief="solid",
                width=80,
                command=lambda q=question: self._on_suggested_question_clicked(q)
            )
            btn.pack(padx=5, pady=5, fill="x")

        # Actualizar el tamaño del canvas después de agregar los botones
        self.questions_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "Tú")

    def _on_suggested_question_clicked(self, question):
        self._insert_message(question, "Tú")

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
