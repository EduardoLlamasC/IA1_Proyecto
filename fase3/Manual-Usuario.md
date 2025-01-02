# Manual de Chatbot

Este archivo describe el funcionamiento, los componentes y las instrucciones para utilizar el chatbot basado en TensorFlow y la librería Tkinter de Python

## Introducción

Este chatbot utiliza un modelo de red neuronal desarrollado con TensorFlow para responder preguntas basándose en patrones definidos en un archivo JSON (`intents.json`). La aplicación incluye:

- Tokenización y normalización de texto de entrada del usuario.
- Entrenamiento de un modelo para identificar intenciones.
- Respuesta al usuario según las intenciones detectadas.

## Estructura del Proyecto

- **main.py**: Archivo principal de la interfaz del chatbot.
- **chat.py**: Archivo que utiliza main.py para cargar el modelo previamente guardado.
- **train.py**: Archivo utilizado para el entrenamiento del modelo.
- **intents.json**: Archivo JSON que contiene patrones de entrada, etiquetas y respuestas posibles.

## Funcionamiento del Código

### 1. Carga de Datos

El archivo `intents.json` es cargado usando la función `loadData`. Este archivo contiene:

- **`patterns`**: Frases de entrada del usuario.
- **`tag`**: Etiqueta asociada a un patrón.
- **`responses`**: Respuestas predefinidas que el bot puede utilizar.

La función convierte estos datos en:

- **Bag of Words** (una representación binaria de la presencia de palabras).
- Etiquetas (“labels”) que corresponden a las intenciones del usuario.

### 2. Tokenización y Procesamiento de Texto

Se utiliza la función `tokenizeAndStem` para:

- **Tokenizar**: Dividir las frases en palabras.
- **Stem**: Reducir palabras a su raíz para normalizar entradas similares.

Por ejemplo:

- Entrada: “Running”.
- Salida: “run”.

### 3. Entrenamiento del Modelo

El modelo es una red neuronal densa creada con TensorFlow.js. El proceso incluye:

- **Estructura del modelo**:

  - Una capa oculta con 8 neuronas y función de activación ReLU.
  - Otra capa oculta con 8 neuronas y activación ReLU.
  - Una capa de salida con tantas neuronas como etiquetas (“labels”) y activación Softmax.

- **Compilación**:

  - Optimizador: `adam`.
  - Pérdida: `categoricalCrossentropy`.

- **Entrenamiento**:
  - Datos de entrada: Representación en “Bag of Words”.
  - Datos de salida: Etiquetas correspondientes.
  - 1000 épocas para asegurar que el modelo generalice correctamente.

### 4. Predicción de Respuestas

La función `predictResponse` utiliza el modelo entrenado para predecir la etiqueta (“tag”) de la entrada del usuario. Basándose en esta etiqueta, selecciona una respuesta aleatoria del archivo `intents.json`.

### 5. Interacción del Usuario

- El usuario ingresa un mensaje en el campo de texto.
- El bot responde en base a su predicción.
- Si el usuario ingresa “quit”, el bot detiene la interacción.

## Requisitos

1. **Archivo `model.keras`**:
   Es el modelo previamente entrenado. Debe estar en la misma ubicación que el archivo main.py y chat.py.

2. Uso de librerías **Tensorflow** y **keras** disponibles en Python.

## Uso

1. Clona el repositorio o descarga los archivos necesarios.
2. Correr el programa con la instrucción `python3 main.py`.
3. Interactuar con el chatbot
4. El chatbot ofrece temas de conversación preestablecidos, para el uso de algoritmos en Python y Javascript.

## Extensiones

- **Mejorar el modelo**:
  Ajusta el número de épocas o la estructura de la red para optimizar resultados.

## Conclusión

Este chatbot es una implementación básica que puede extenderse para tareas más complejas, como la integración de procesamiento de lenguaje natural avanzado o la carga de modelos previamente entrenados.

## ANEXOS

![image](/assets/chatbot1.jpg)
![image](/assets/chatbot2.jpg)
![image](/assets/chatbot3.jpg)
