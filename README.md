# Transcripción de Micrófono en Tiempo Real con Sherpa-ONNX

Aplicación de Python simple, modular y ligera para reconocimiento de voz a texto en tiempo real

Utiliza [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).

- **100% Local y Offline**: No requiere APIs en la nube ni conexión a internet una vez descargados los modelos.
- **Optimizado para CPU (sin GPU requerida)**: Funciona en equipos de dos núcleos de gama baja y dispositivos embebidos utilizando modelos Zipformer de *streaming* cuantizados en `int8`.
- **Salida directa de Sherpa (*Raw*)**: Emite la salida estructurada completa y sin modificaciones de sherpa-onnx (texto, subtokens, marcas de tiempo, estado de endpoint).
- **Diseño modular**: La captura de audio, el reconocimiento de voz y el despacho de resultados están desacoplados, lo que facilita enviar la transcripción a una interfaz web (mediante WebSocket, SSE, FastAPI, etc.).

---

Version 1

Utilizada en la charla del 22 de Septiembre del 2026 sobre artistas que hacen software en el centro cultural de la UNC en la que participaron Constanza Chiappini, Lola Granillo y Sergio Scotta

---

## Inicio Rápido

### 1. Iniciar con un solo comando (Windows)

Simplemente ejecuta:
```cmd
run.bat
```
*(En el primer inicio, `run.bat` crea automáticamente el entorno virtual e instala las dependencias).*

O utilizando Python directamente:
```powershell
.\venv\Scripts\python main.py
```

### 2. Idiomas disponibles

La aplicación viene preconfigurada con dos modelos de *streaming* rápidos y optimizados para CPU:

- **Español (Predeterminado)**:
  ```powershell
  python main.py --lang es
  ```

- **Inglés**:
  ```powershell
  python main.py --lang en
  ```
  *(Utiliza un modelo Zipformer de 20M cuantizado en `int8`, usando menos de 100 MB de RAM).*

---

## Formatos de Salida

Puedes elegir cómo se presenta la salida en la consola usando `--format`:

### 1. Formato Raw (`--format raw`, Predeterminado)
Muestra cada actualización de voz y endpoint directamente como la cadena JSON sin procesar de sherpa-onnx:
```
[PARTIAL] { "text": "HOLA", "tokens": [" HOLA"], "timestamps": [0.48], ... }
[PARTIAL] { "text": "HOLA MUNDO", "tokens": [" HOLA", " MUNDO"], "timestamps": [0.48, 0.96], ... }
[ENDPOINT] { "text": "HOLA MUNDO", "tokens": [" HOLA", " MUNDO"], "timestamps": [0.48, 0.96], ... }
```

### 2. JSON Formateado (`--format json`)
Muestra JSON indentado con campos de alto nivel y metadatos completos:
```json
{
  "status": "[ENDPOINT]",
  "segment_id": 1,
  "text": "HOLA MUNDO",
  "tokens": [" HOLA", " MUNDO"],
  "timestamps": [0.48, 0.96],
  "is_endpoint": true,
  "raw_sherpa": { ... }
}
```

### 3. Modo Compacto (`--format compact`)
Visualización limpia en una sola línea en tiempo real en la terminal:
```
[Seg 00...] Hola mundo
[Seg 01] ¡Hola mundo!
```

---

## Selección de Micrófono

Para listar todos los micrófonos conectados:
```powershell
python main.py --list-devices
```

Salida de ejemplo:
```
Available Audio Input Devices:
-----------------------------------------------------------------
ID   Default   Channels   Name
-----------------------------------------------------------------
1    [*]       4          Microphone Array (Intel Smart Sound)
13             2          External USB Microphone
-----------------------------------------------------------------
```

Especifica un dispositivo indicando `--device <ID>`:
```powershell
python main.py --device 13
```

---

## Referencia de Opciones de la CLI

| Parámetro | Valor por defecto | Descripción |
|------|---------|-------------|
| `--lang {en, es}` | `es` | Idioma del modelo preconfigurado (`es` [predeterminado] o `en`). |
| `--model-dir PATH` | `None` | Directorio personalizado que contiene `encoder`, `decoder`, `joiner` y `tokens.txt`. |
| `--format {raw, json, compact}` | `raw` | Formato de salida en la consola. |
| `--device ID` | Micrófono por defecto | ID del dispositivo de micrófono a utilizar. |
| `--list-devices` | `False` | Lista los dispositivos de entrada de audio disponibles y sale. |
| `--threads INT` | `2` | Número de hilos de CPU para inferencia. |
| `--sample-rate INT` | `16000` | Frecuencia de muestreo de audio en Hz. |

---

## Estructura del Proyecto y Modularidad

```
cc-unc/
├── main.py                  # Punto de entrada de la CLI
├── run.bat                  # Lanzador en 1 clic para Windows
├── requirements.txt         # Dependencias (sherpa-onnx, sounddevice, numpy)
├── models/                  # Archivos de modelos ONNX descargados (ignorado en git)
│   ├── sherpa-onnx-streaming-zipformer-en-20M-2023-02-17/
│   └── sherpa-onnx-streaming-zipformer-es-kroko-2025-08-06/
├── src/
│   ├── app.py               # Orquestador SpeechRecognitionApp
│   ├── audio_stream.py      # Captura de micrófono con sounddevice
│   ├── recognizer.py        # Motor OnlineRecognizer de sherpa-onnx
│   ├── model_manager.py     # Detección y descarga automática de modelos
│   ├── callbacks.py         # Despachadores de salida (Consola, WebSocket, etc.)
│   ├── events.py            # Dataclass TranscriptionResult
│   └── config.py            # Configuración de audio y modelo
└── tests/
    └── test_components.py   # Suite de pruebas automatizadas con pytest
```

---

## Conexión mediante WebSocket (Guía para Interfaz Web)

Cuando estés listo para conectar este servicio a una interfaz web, ten en cuenta los siguientes puntos:

### Aspectos Clave a Considerar:

1. **Integración de Hilos y Asyncio**:
   - `SpeechRecognitionApp.run()` opera en un bucle sincrónico y bloqueante leyendo desde `sounddevice`.
   - Los frameworks web (FastAPI, Starlette, websockets) se ejecutan sobre un bucle de eventos `asyncio`.
   - **Patrón Recomendado**: Ejecutar `app.run()` en un hilo de fondo (`threading.Thread`) y reenviar los mensajes al bucle asincrónico usando `asyncio.run_coroutine_threadsafe()` o una cola segura entre hilos.

2. **Transcripciones Provisionales vs. Finales**:
   - Inspecciona `result.is_endpoint`:
     - `False`: Transcripción parcial/en curso (transmítela a la interfaz para dar retroalimentación visual inmediata a medida que el usuario habla).
     - `True`: Frase finalizada (silencio detectado). La interfaz puede consolidar este segmento y reiniciar su búfer activo.

3. **Esquema de Mensajes**:
   - Usa `result.to_dict()` para una serialización JSON consistente. Produce:
     ```json
     {
       "text": "texto de la transcripción",
       "segment_id": 1,
       "is_endpoint": false,
       "tokens": ["..."],
       "timestamps": [0.48, 0.96],
       "raw": { ... }
     }
     ```

4. **Desconexiones de Clientes**:
   - Asegúrate de que los errores al enviar por WebSocket (por ejemplo, cuando se cierra una pestaña del navegador) no detengan el bucle de reconocimiento. Captura las excepciones dentro de tu callback personalizado.

### Ejemplo de Integración (FastAPI / WebSocket):

```python
import asyncio
import threading
from fastapi import FastAPI, WebSocket
from src.app import SpeechRecognitionApp
from src.callbacks import CallableOutputCallback
from src.config import AppConfig
from src.model_manager import resolve_model

app = FastAPI()
active_connections: list[WebSocket] = []

def broadcast_transcription(result, loop):
    payload = result.to_dict()
    for ws in list(active_connections):
        asyncio.run_coroutine_threadsafe(ws.send_json(payload), loop)

@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantiene la conexión abierta
    finally:
        active_connections.remove(websocket)

# Para iniciar el reconocedor junto con el servidor:
loop = asyncio.get_event_loop()
rec_app = SpeechRecognitionApp(
    config=AppConfig(),
    model_config=resolve_model(lang="es"),
    callbacks=[CallableOutputCallback(lambda res: broadcast_transcription(res, loop))]
)
threading.Thread(target=rec_app.run, daemon=True).start()
```