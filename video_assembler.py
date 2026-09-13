import subprocess
import os

def obtener_duracion_audio(audio_path: str) -> float:
    """
    Obtiene la duración exacta de un archivo de audio utilizando ffprobe.
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    resultado = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
    return float(resultado.stdout.strip())

def crear_video_short(imagen_path: str, audio_path: str, output_path: str = "output_short.mp4"):
    """
    Genera un video vertical 9:16 (1080x1920) aplicando un efecto zoom Ken Burns
    y sincronizándolo con la duración del audio.
    """
    if not os.path.exists(imagen_path):
        raise FileNotFoundError(f"No se encontró la imagen en: {imagen_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"No se encontró el audio en: {audio_path}")
        
    duracion = obtener_duracion_audio(audio_path) + 0.5  # Margen final de seguridad
    total_frames = int(duracion * 30)

    print(f"[*] Renderizando video vertical (Duración total: {duracion:.2f}s)...")

    # Comando FFmpeg optimizado para bajo consumo de memoria RAM
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
        "-ar", "44100",
        "-ac", "2",
        "-shortest",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"[✔] Video final exportado exitosamente en: {output_path}")

if __name__ == "__main__":
    crear_video_short("assets/sample_image.jpg", "assets/speech.wav")
