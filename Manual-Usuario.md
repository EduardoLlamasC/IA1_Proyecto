
# Manual de Chatbot

Este archivo describe el funcionamiento, los componentes y las instrucciones para utilizar el chatbot basado en HTML, JavaScript y TensorFlow.js incluido en este proyecto.

## Introducción

Este chatbot utiliza un modelo de red neuronal desarrollado con TensorFlow.js para responder preguntas basándose en patrones definidos en un archivo JSON (`intents.json`). La aplicación incluye:

- Tokenización y normalización de texto de entrada del usuario.
- Entrenamiento de un modelo para identificar intenciones.
- Respuesta al usuario según las intenciones detectadas.

## Estructura del Proyecto

- **index.html**: Archivo principal de la interfaz del chatbot.
- **intents.json**: Archivo JSON que contiene patrones de entrada, etiquetas y respuestas posibles.
- **TensorFlow.js**: Librería utilizada para desarrollar y entrenar la red neuronal.

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

1. **Librería TensorFlow.js**:
   Incluida en el proyecto mediante:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
   ```

2. **Archivo `intents.json`**:
   Debe estar en la misma ubicación que el archivo HTML.

   Ejemplo de estructura:
   ```json
   {
       "intents": [
           {
               "tag": "saludo",
               "patterns": ["Hola", "¿Cómo estás?"],
               "responses": ["Hola, ¿en qué puedo ayudarte?", "¡Hola!"]
           }
       ]
   }
   ```

## Uso

1. Clona el repositorio o descarga los archivos necesarios.
2. Asegúrate de incluir el archivo `intents.json` en el mismo directorio.
3. Abre el archivo `index.html` en un navegador web.
4. Espera a que el modelo se cargue (mensaje: “Loading model...”).
5. Una vez cargado, ingresa un mensaje en el campo de texto y haz clic en el botón “Send”.

## Extensiones

- **Agregar nuevas intenciones**:
  Modifica el archivo `intents.json` para agregar nuevos patrones, etiquetas y respuestas.

- **Mejorar el modelo**:
  Ajusta el número de épocas o la estructura de la red para optimizar resultados.

## Conclusión

Este chatbot es una implementación básica que puede extenderse para tareas más complejas, como la integración de procesamiento de lenguaje natural avanzado o la carga de modelos previamente entrenados. 

## ANEXOS
![image](https://github.com/user-attachments/assets/a0e94013-c363-4173-9956-e2492ce7d456)
![image](https://github.com/user-attachments/assets/5cd285cc-59ce-4688-8efb-f94aeed8677f)

