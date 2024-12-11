# IA1_Proyecto

# Manual Técnico 

## Estructura del Proyecto

1. **intents.json**: Archivo JSON con las intenciones, patrones y respuestas.
2. **Código JavaScript**: Contiene la lógica para entrenar el modelo, predecir respuestas y manejar las interacciones con el usuario.
3. **HTML**: Interfaz de usuario básica para interactuar con el chatbot.

---

## Flujo de Ejecución

### 1. **Carga de Datos**

Se carga el archivo `intents.json` que contiene los patrones y las respuestas asociadas a cada intención.

```js
async function loadData() {
    const response = await fetch('intents.json');
    intentsData = await response.json();
    // Procesa los datos...
}
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

```js
function tokenizeAndStem(sentence) {
    const wordsInSentence = sentence
        .toLowerCase()
        .replace(/[^\w\s]/g, '')  // Elimina caracteres especiales
        .split(/\s+/);  // Divide la frase en palabras

    return wordsInSentence.map(word => stem(word)).filter(word => word !== "?");
}

function stem(word) {
    if (word.endsWith('es')) {
        return word.slice(0, -2);
    } else if (word.endsWith('ed')) {
        return word.slice(0, -2);
    } else if (word.endsWith('ing')) {
        return word.slice(0, -3);
    } else {
        return word;
    }
}
```

### 3. **Entrenamiento del Modelo**

El modelo se entrena utilizando **TensorFlow.js** con los datos preprocesados. Se usa una red neuronal con dos capas ocultas de 8 unidades y la función de activación `relu`. La salida tiene tantas neuronas como intenciones posibles.

```js
async function trainModel(trainingData, outputData) {
    const model = tf.sequential();
    model.add(tf.layers.dense({ units: 8, inputShape: [trainingData[0].length], activation: 'relu' }));
    model.add(tf.layers.dense({ units: 8, activation: 'relu' }));
    model.add(tf.layers.dense({ units: labels.length, activation: 'softmax' }));

    model.compile({ loss: 'categoricalCrossentropy', optimizer: 'adam', metrics: ['accuracy'] });

    const xs = tf.tensor(trainingData);
    const ys = tf.tensor(outputData);

    await model.fit(xs, ys, {
        epochs: 1000,
        batchSize: 8,
        verbose: 1
    });

    return model;
}
```

### 4. **Predicción de Respuesta**

El modelo predice la intención del mensaje ingresado por el usuario. La entrada se convierte en un "bag of words" (bolsa de palabras), que es un vector binario de 0s y 1s indicando si una palabra de la entrada está presente en el vocabulario entrenado.

```js
async function predictResponse(input) {
    const bag = words.map(word => (input.includes(word) ? 1 : 0));
    const prediction = await model.predict(tf.tensor([bag]));
    const predictedIndex = prediction.argMax(1).dataSync()[0];
    const predictedTag = labels[predictedIndex];

    const intent = intentsData.intents.find(intent => intent.tag === predictedTag);
    return intent.responses[Math.floor(Math.random() * intent.responses.length)];
}
```

### 5. **Interacción con el Usuario**

El usuario escribe un mensaje y el chatbot responde de acuerdo a la predicción del modelo. La entrada del usuario es tomada de un campo de texto, y la respuesta se muestra en la interfaz.

```js
async function sendMessage() {
    const userInput = document.getElementById('user_input').value;
    if (userInput.toLowerCase() === 'quit') {
        return;
    }

    const response = await predictResponse(userInput);
    document.getElementById('chat').innerHTML += `<div><strong>Tu:</strong> ${userInput}</div>`;
    document.getElementById('chat').innerHTML += `<div><strong>Bot:</strong> ${response}</div>`;
}

---

## Descripción de Funciones

1. **`loadData()`**: Carga y preprocesa los datos de `intents.json`, genera el vocabulario y prepara los datos para el entrenamiento.
2. **`tokenizeAndStem(sentence)`**: Convierte una frase en una lista de palabras procesadas.
3. **`trainModel(trainingData, outputData)`**: Entrena el modelo con los datos procesados utilizando una red neuronal de TensorFlow.js.
4. **`predictResponse(input)`**: Realiza una predicción de la respuesta del chatbot basada en la entrada del usuario.
5. **`sendMessage()`**: Obtiene la entrada del usuario, predice la respuesta del modelo y la muestra en la interfaz.
6. **`stem(word)`**: Aplica un proceso básico de stemming para reducir las palabras a su raíz.
