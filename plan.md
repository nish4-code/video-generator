Plan Técnico: Generador Automatizado de Videos Cortos (Bajo Consumo de RAM)

Este plan detalla el paso a paso para construir un generador de videos verticales (9:16) en local utilizando Python, Kokoro-TTS (voz natural de bajo peso) y FFmpeg (ensamblado de video y animación Ken Burns). El pipeline completo consume menos de 4 GB de RAM.

1. Requisitos del Sistema y Dependencias

Requisitos

Sistema Operativo: Linux (Ubuntu/Debian) o WSL2 / macOS / Windows

Memoria RAM disponible: 4 GB o superior

Almacenamiento: ~1.5 GB libres

Dependencias del Sistema

Asegúrate de contar con ffmpeg y Python 3.10+:

# En Debian/Ubuntu/WSL
sudo apt update && sudo apt install -y ffmpeg python3-venv python3-pip

# En macOS (con Homebrew)
brew install ffmpeg python


2. Preparación del Entorno de Trabajo

Ejecuta estos comandos en tu terminal para aislar las dependencias:

mkdir -p video_generator && cd video_generator
python3 -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\Activate.ps1

# Instalación de librerías ligeras
pip install kokoro soundfile numpy pillow


3. Estructura del Proyecto

video_generator/
├── venv/
├── assets/
│   ├── sample_image.jpg     # Imagen de fondo vertical (1080x1920)
│   └── background_audio.mp3 # Música de fondo suave (opcional)
├── voice_generator.py       # Generación de voz con Kokoro-TTS
├── video_assembler.py       # Montaje con FFmpeg (Zoom + Audio)
└── main.py                  # Orquestador del pipeline


4. Código Fuente

voice_generator.py (Síntesis de Voz Ligera)

import soundfile as sf
from kokoro import KPipeline

def generar_audio(texto: str, output_path: str = "assets/speech.wav", lang_code: str = "e", voice: str = "em_alex"):
    """
    Genera audio usando Kokoro-TTS.
    lang_code 'e': Español (es)
    voice: em_alex, em_santa, ef_dora, etc.
    """
    print(f"[*] Sintetizando voz ({voice})...")
    pipeline = KPipeline(lang_code=lang_code)
    
    generator = pipeline(texto, voice=voice, speed=1.0, split_pattern=r'\n+')
    audio_segments = []
    
    for _, _, audio in generator:
        audio_segments.append(audio)
        
    if not audio_segments:
        raise ValueError("No se pudo generar el audio a partir del texto provisto.")
        
    import numpy as np
    final_audio = np.concatenate(audio_segments)
    sf.write(output_path, final_audio, 24000)
    print(f"[✔] Audio guardado exitosamente en: {output_path}")
    return output_path

if __name__ == "__main__":
    texto_ejemplo = "¿Sabías que el primer procesador comercial de la historia, el Intel 4004, tenía una velocidad de reloj de apenas 740 kilohercios? Hoy, tu teléfono es millones de veces más rápido."
    generar_audio(texto_ejemplo)


video_assembler.py (Montaje Dinámico con FFmpeg)

Este script toma la imagen, aplica un efecto de zoom lento y continuo (Ken Burns), e inserta el audio generado sin saturar la memoria RAM.

import subprocess
import os

def obtener_duracion_audio(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    resultado = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(resultado.stdout.decode().strip())

def crear_video_short(imagen_path: str, audio_path: str, output_path: str = "output_short.mp4"):
    duracion = obtener_duracion_audio(audio_path) + 0.5  # Margen de 0.5s al final
    total_frames = int(duracion * 30)

    print(f"[*] Renderizando video vertical (Duración: {duracion:.2f}s)...")

    # Comando FFmpeg para zoom dinámico 1080x1920 (9:16)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", imagen_path,
        "-i", audio_path,
        "-filter_complex",
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920:fps=30[v]",
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-t", str(duracion),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"[✔] Video final exportado en: {output_path}")

if __name__ == "__main__":
    crear_video_short("assets/sample_image.jpg", "assets/speech.wav")


main.py (Pipeline Completo)

import os
from PIL import Image, ImageDraw, ImageFont
from voice_generator import generar_audio
from video_assembler import crear_video_short

def crear_imagen_base_si_no_existe(path: str = "assets/sample_image.jpg"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        print("[*] Creando imagen vertical de muestra...")
        img = Image.new("RGB", (1080, 1920), color=(20, 24, 35))
        draw = ImageDraw.Draw(img)
        # Dibujar elementos gráficos simples
        draw.rectangle([(80, 80), (1000, 1840)], outline=(50, 100, 200), width=8)
        img.save(path, quality=95)

def ejecutar_pipeline():
    crear_imagen_base_si_no_existe()
    
    guion = (
        "Tres datos tecnológicos que probablemente no conocías. "
        "Número uno: El primer disco duro de cinco megabytes pesaba más de una tonelada. "
        "Número dos: Más del noventa por ciento del dinero del mundo existe solo en formato digital."
    )
    
    audio_file = "assets/speech.wav"
    imagen_file = "assets/sample_image.jpg"
    video_file = "short_demo.mp4"
    
    generar_audio(texto=guion, output_path=audio_file)
    crear_video_short(imagen_path=imagen_file, audio_path=audio_file, output_path=video_file)

if __name__ == "__main__":
    ejecutar_pipeline()


5. Ejecución y Prueba

Guarda los archivos en la carpeta video_generator/.

Ejecuta el pipeline:

python main.py


Resultado: Se generará el archivo short_demo.mp4 listo para reproducir o subir a plataformas verticales.