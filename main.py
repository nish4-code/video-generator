import os
from PIL import Image, ImageDraw
from voice_generator import generar_audio
from video_assembler import crear_video_short

def crear_imagen_base_si_no_existe(path: str = "assets/sample_image.jpg"):
    """
    Crea una imagen vertical (1080x1920) de muestra en caso de no existir.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        print("[*] Generando imagen vertical de muestra (1080x1920)...")
        img = Image.new("RGB", (1080, 1920), color=(20, 24, 35))
        draw = ImageDraw.Draw(img)
        # Dibujar un marco decorativo
        draw.rectangle([(80, 80), (1000, 1840)], outline=(50, 100, 200), width=8)
        img.save(path, quality=95)
        print(f"[✔] Imagen guardada en: {path}")

def ejecutar_pipeline():
    """
    Orquesta el flujo completo de generación de audio y ensamble de video vertical.
    """
    crear_imagen_base_si_no_existe()
    
    guion = (
        "Tres datos tecnológicos que probablemente no conocías. "
        "Número uno: El primer disco duro de cinco megabytes pesaba más de una tonelada. "
        "Número dos: Más del noventa por ciento del dinero del mundo existe solo en formato digital."
    )
    
    audio_file = "assets/speech.wav"
    imagen_file = "assets/sample_image.jpg"
    video_file = "short_demo.mp4"
    
    # 1. Generar la voz sintética
    generar_audio(texto=guion, output_path=audio_file)
    
    # 2. Renderizar el video vertical
    crear_video_short(imagen_path=imagen_file, audio_path=audio_file, output_path=video_file)
    
    print("\n==========================================")
    print(f"¡Proceso completado! Archivo final: {video_file}")
    print("==========================================\n")

if __name__ == "__main__":
    ejecutar_pipeline()
