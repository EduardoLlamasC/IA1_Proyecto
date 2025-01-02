# IA1_Proyecto

https://drive.google.com/drive/folders/1rl7aqI9j8XEQK2943phIHeG5CEnaVQuP?usp=sharing

# Manual Técnico

## Estructura del Proyecto

- **main.py**: Archivo principal de la interfaz del chatbot.
- **chat.py**: Archivo que utiliza main.py para cargar el modelo previamente guardado.
- **train.py**: Archivo utilizado para el entrenamiento del modelo.
- **intents.json**: Archivo JSON que contiene patrones de entrada, etiquetas y respuestas posibles.

---

## Flujo de Ejecución

### 1. **Carga de Datos**

Se carga el archivo `intents.json` que contiene los patrones y las respuestas asociadas a cada intención.

```py
with open('intents.json') as content:
    data = json.load(content)
```

El archivo `intents.json` tiene un formato como:

```json
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["Hi", "Hello", "How are you?"],
      "responses": ["Hello!", "Hi there!", "Good to see you!"]
    },
    {
      "tag": "goodbye",
      "patterns": ["Goodbye", "See you later", "Bye"],
      "responses": ["Goodbye!", "Take care!", "See you soon!"]
    }
  ]
}
```

### 2. **Preprocesamiento de Texto**

Se realiza un preprocesamiento sobre los patrones de las intenciones: tokenización, conversión a minúsculas y "stemming" (reducción a la raíz de las palabras).

```py
tags = []
patterns = []
responses = {}

for intent in data['intents']:
    responses[intent['tag']] = intent['responses']

    for line in intent['patterns']:
        patterns.append(line)
        tags.append(intent['tag'])

data = pd.DataFrame({"patterns": patterns, "tags":tags})
data['patterns'] = data['patterns'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['patterns'] = data['patterns'].apply(lambda wrd: ''.join(wrd))

tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['patterns'])
train = tokenizer.texts_to_sequences(data['patterns'])

x_train = pad_sequences(train)

le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

input_shape = x_train.shape[1]

vocabulary = len(tokenizer.word_index)
output_lenght = le.classes_.shape[0]

i = Input(shape=(input_shape,))
x = Embedding(vocabulary+1, 10)(i)
x = LSTM(10,return_sequences=True)(x)
x = Flatten()(x)
x = Dense(output_lenght,activation='softmax')(x)
model = Model(i, x)

model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

model.fit(x_train, y_train, epochs=200)

print(model.summary())

model.save('model.keras')
```

### 3. **Entrenamiento del Modelo**

El modelo se entrena utilizando **TensorFlow.js** con los datos preprocesados. Se usa una red neuronal con dos capas ocultas de 8 unidades y la función de activación `relu`. La salida tiene tantas neuronas como intenciones posibles.

```py
import json
import string
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input, Flatten
from tensorflow.keras.models import Model
from sklearn.preprocessing import LabelEncoder

with open('intents.json') as content:
    data = json.load(content)

tags = []
patterns = []
responses = {}

for intent in data['intents']:
    responses[intent['tag']] = intent['responses']

    for line in intent['patterns']:
        patterns.append(line)
        tags.append(intent['tag'])

data = pd.DataFrame({"patterns": patterns, "tags":tags})
data['patterns'] = data['patterns'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['patterns'] = data['patterns'].apply(lambda wrd: ''.join(wrd))

tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['patterns'])
train = tokenizer.texts_to_sequences(data['patterns'])

x_train = pad_sequences(train)

le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

input_shape = x_train.shape[1]

vocabulary = len(tokenizer.word_index)
output_lenght = le.classes_.shape[0]

i = Input(shape=(input_shape,))
x = Embedding(vocabulary+1, 10)(i)
x = LSTM(10,return_sequences=True)(x)
x = Flatten()(x)
x = Dense(output_lenght,activation='softmax')(x)
model = Model(i, x)

model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

model.fit(x_train, y_train, epochs=200)

print(model.summary())

model.save('model.keras')

```

### 4. **Predicción de Respuesta**

El modelo predice la intención del mensaje ingresado por el usuario. La entrada se convierte en un "bag of words" (bolsa de palabras), que es un vector binario de 0s y 1s indicando si una palabra de la entrada está presente en el vocabulario entrenado.

```py
def get_prediction(prediction_input):
    texts_p = []

    prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)

    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input], input_shape)

    output = model.predict(prediction_input)
    output = output.argmax()

    response_tag = le.inverse_transform([output])[0]
    return random.choice(responses[response_tag])

```

### 5. **Interacción con el Usuario**

El usuario escribe un mensaje y el chatbot responde de acuerdo a la predicción del modelo. La entrada del usuario es tomada de un campo de texto, y la respuesta se muestra en la interfaz.

```py
import numpy as np
import pandas as pd
import string
import json
import random

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder

with open('intents.json') as content:
    data = json.load(content)

tags = []
patterns = []
responses = {}

for intent in data['intents']:
    responses[intent['tag']] = intent['responses']

    for line in intent['patterns']:
        patterns.append(line)
        tags.append(intent['tag'])

data = pd.DataFrame({"patterns": patterns, "tags":tags})
data['patterns'] = data['patterns'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['patterns'] = data['patterns'].apply(lambda wrd: ''.join(wrd))

tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['patterns'])
train = tokenizer.texts_to_sequences(data['patterns'])

x_train = pad_sequences(train)

le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

input_shape = x_train.shape[1]

vocabulary = len(tokenizer.word_index)
output_lenght = le.classes_.shape[0]

model = load_model('./model.keras')

model.summary()

def get_prediction(prediction_input):
    texts_p = []

    prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)

    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input], input_shape)

    output = model.predict(prediction_input)
    output = output.argmax()

    response_tag = le.inverse_transform([output])[0]
    return random.choice(responses[response_tag])
```
