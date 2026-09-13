# Generador de Videos Cortos de Alta Retención v2.0 (Debian Linux)

Este sistema genera automáticamente **videos verticales (9:16 - 1080x1920)** optimizados para **TikTok, YouTube Shorts y Instagram Reels**, sustituyendo las imágenes estáticas por un pipeline de producción multimedia dinámico:

1. **Multiescenas con Clips en Movimiento (`.mp4`)**: Cambios de escena cada 2 a 4 segundos.
2. **Subtítulos Dinámicos Karaoke (Alex Hormozi / TikTok)**: Las palabras se destacan en amarillo neón exactamente al ritmo del audio.
3. **Personaje / Avatar Animado Superpuesto**: Avatar animado colocado en la esquina inferior.
4. **Audio Alta fidelidad**: Voces con **Kokoro-TTS** en español resampleadas a 44.1 kHz estéreo AAC.

---

## 1. Requisitos e Instalación en Debian

### Paso 1: Dependencias del Sistema
```bash
sudo apt update && sudo apt install -y \
    ffmpeg \
    python3 \
    python3-pip \
    python3-venv \
    libsndfile1 \
    espeak-ng
```

### Paso 2: Entorno Virtual e Instalación de Librerías Python
```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Configuración Opcional (Clips de Stock HD)

Si deseas descargar automáticamente clips de video HD reales según las palabras del guion, puedes utilizar la API gratuita de Pexels:

1. Consigue una API Key gratuita en [pexels.com/api](https://www.pexels.com/api/).
2. Exporta tu clave en la terminal antes de ejecutar:

```bash
export PEXELS_API_KEY="tu_clave_de_pexels_aqui"
```

*Nota: Si no defines una API Key, el sistema genera automáticamente clips de video procedimentales animados en movimiento sin fallar.*

---

## 3. Estructura del Proyecto v2.0

```text
video_generator/
├── requirements.txt         # Librerías necesarias (kokoro, soundfile, requests, pillow)
├── script_parser.py         # Divide el guion en escenas cortas con palabras clave
├── stock_fetcher.py         # Descarga o genera clips MP4 en movimiento por escena
├── subtitles_generator.py   # Genera subtítulos Karaoke .ASS animados estilo Alex Hormozi
├── avatar_overlay.py        # Genera/Carga el personaje animado superpuesto
├── video_engine.py          # Ensambla clips, avatar, audio 44.1kHz estéreo y subtítulos
├── voice_generator.py       # Síntesis de voz en español con Kokoro-TTS
├── main.py                  # Orquestador del pipeline v2.0
└── assets/                  # Guardado de clips, avatar, audio speech.wav y subtítulos
```

---

## 4. Ejecución

Con el entorno virtual activado (`source venv/bin/activate`):

```bash
python3 main.py
```

El resultado final se guardará en **`short_v2_demo.mp4`**.

---

## 5. Personalizar el Personaje

Si deseas usar tu propia caricatura o personaje:
Coloca una imagen con fondo transparente PNG (400x400 px) en **`assets/avatar/character.png`** antes de ejecutar `main.py`. El sistema la utilizará automáticamente como el personaje animado del video.
