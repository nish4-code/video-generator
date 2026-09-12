# Generador Automatizado de Videos Cortos (Debian Linux)

Este proyecto permite generar automatizadamente videos verticales en formato 9:16 (1080x1920) listos para redes sociales (TikTok, YouTube Shorts, Reels), utilizando sintesis de voz natural en español (**Kokoro-TTS**) y ensamblado dinámico con animación Ken Burns mediante **FFmpeg**.

El pipeline está especialmente optimizado para ejecutarse en entornos con **bajo consumo de memoria RAM (< 4 GB)**.

---

## 1. Requisitos e Instalación en Debian

Ejecuta los siguientes pasos en la terminal de tu sistema **Debian Linux** (Debian 11 Bullseye / Debian 12 Bookworm) o distribuciones derivadas (Ubuntu, Linux Mint, Pop!_OS):

### Paso 1: Instalar Paquetes del Sistema
Actualiza los repositorios e instala las dependencias de sistema necesarias (`ffmpeg`, soporte para archivos de audio WAV, motor `espeak-ng` y entorno virtual de Python):

```bash
sudo apt update && sudo apt install -y \
    ffmpeg \
    python3 \
    python3-pip \
    python3-venv \
    libsndfile1 \
    espeak-ng
```

### Paso 2: Crear y Activar el Entorno Virtual
Ubícate en la carpeta del proyecto y crea un entorno aislado de Python:

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

### Paso 3: Instalar Dependencias de Python
Con el entorno virtual activado, instala las librerías necesarias ejecutando:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Estructura del Proyecto

```text
video_generator/
├── requirements.txt         # Lista de dependencias Python (kokoro, soundfile, pillow, numpy)
├── voice_generator.py       # Síntesis de voz con Kokoro-TTS (Español)
├── video_assembler.py       # Renderizado de video vertical 9:16 con FFmpeg
├── main.py                  # Orquestador del pipeline completo
├── README.md                # Guía de instalación y uso en Debian
└── assets/                  # Carpeta de recursos generados (imágenes, audio speech.wav)
```

---

## 3. Ejecución y Prueba

Para ejecutar el pipeline completo de prueba:

```bash
# Asegúrate de tener el entorno virtual activado (source venv/bin/activate)
python3 main.py
```

### ¿Qué hace `main.py`?
1. Crea automáticamente una imagen vertical de muestra (`assets/sample_image.jpg`) si no existe ninguna.
2. Genera la voz sintética a partir de un texto de muestra en español usando Kokoro-TTS y la guarda en `assets/speech.wav`.
3. Calcula la duración del audio y genera el archivo final `short_demo.mp4` aplicando un efecto visual de zoom continuo (Ken Burns) sin sobrecargar la RAM.

---

## 4. Personalización

* **Cambiar el Guion**: Edita la variable `guion` dentro de `main.py` o importa `generar_audio()` en tus propios scripts.
* **Usar tu propia imagen de fondo**: Coloca tu imagen vertical (1080x1920 en formato `.jpg` o `.png`) en `assets/sample_image.jpg` antes de ejecutar el programa.
* **Cambiar la voz de síntesis**: En `voice_generator.py` puedes ajustar el parámetro `voice` por cualquier voz compatible con Kokoro en español (ejemplo: `em_alex`, `em_santa`, `ef_dora`).

---

## 5. Solución de Problemas Comunes en Debian

* **Error `OSError: sndfile library not found`**:
  Ocurre si falta la librería `libsndfile1` en Debian. Instálala ejecutando: `sudo apt install libsndfile1`.

* **Error `ffmpeg: command not found`**:
  Asegúrate de haber instalado FFmpeg: `sudo apt install ffmpeg`.

* **Permisos del entorno virtual**:
  Si `python3 -m venv venv` falla, asegúrate de instalar `python3-venv`: `sudo apt install python3-venv`.
