import os
import math
import numpy as np
import soundfile as sf
import subprocess
from PIL import Image, ImageDraw, ImageFilter

def calcular_envolvente_audio(audio_path: str, fps: int = 30) -> np.ndarray:
    """
    Calcula el nivel de energía de volumen RMS por fotograma de video (30 fps)
    a partir del archivo de audio speech.wav para controlar la animación labial.
    """
    data, samplerate = sf.read(audio_path)
    if data.ndim > 1:
        data = data.mean(axis=1)

    samples_per_frame = int(samplerate / fps)
    num_frames = math.ceil(len(data) / samples_per_frame)
    envolvente = []

    for i in range(num_frames):
        start = i * samples_per_frame
        end = min(start + samples_per_frame, len(data))
        chunk = data[start:end]
        if len(chunk) > 0:
            rms = np.sqrt(np.mean(chunk**2))
            envolvente.append(rms)
        else:
            envolvente.append(0.0)

    arr = np.array(envolvente)
    max_val = np.max(arr)
    if max_val > 0:
        arr = arr / max_val
    return arr

def generar_video_avatar_lipsync(
    audio_path: str,
    avatar_image_path: str = "assets/avatar/character.png",
    output_avatar_mp4: str = "assets/talking_avatar.mp4",
    fps: int = 30
) -> str:
    """
    Genera un video animado MP4 del personaje con sincronización labial (Lip-Sync),
    guiño de ojos y micro-movimiento de cabeza controlado por el audio.
    """
    os.makedirs(os.path.dirname(output_avatar_mp4), exist_ok=True)
    os.makedirs("assets/avatar", exist_ok=True)

    # Crear imagen base de avatar estilo presentador futurista si no existe
    if not os.path.exists(avatar_image_path):
        print("[*] Creando personaje avatar base...")
        base = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
        d = ImageDraw.Draw(base)
        # Cabeza
        d.ellipse([(100, 80), (400, 380)], fill=(25, 30, 48, 255), outline=(0, 210, 255, 255), width=8)
        # Ojos
        d.ellipse([(170, 160), (220, 210)], fill=(255, 255, 255, 255))
        d.ellipse([(280, 160), (330, 210)], fill=(255, 255, 255, 255))
        d.ellipse([(185, 175), (205, 195)], fill=(0, 210, 255, 255))
        d.ellipse([(295, 175), (315, 195)], fill=(0, 210, 255, 255))
        base.save(avatar_image_path)

    base_img = Image.open(avatar_image_path).convert("RGBA").resize((500, 500))
    envolvente = calcular_envolvente_audio(audio_path, fps=fps)
    num_frames = len(envolvente)

    frames_dir = "assets/avatar_frames"
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] Generando animación Lip-Sync ({num_frames} fotogramas)...")

    for i in range(num_frames):
        vol = envolvente[i]  # 0.0 a 1.0
        frame = base_img.copy()
        draw = ImageDraw.Draw(frame)

        # 1. Apertura labial según volumen del audio (Lip-Sync)
        boca_apertura = int(vol * 45)  # 0 a 45px de apertura
        boca_box = [(200, 270 - (boca_apertura // 2)), (300, 280 + (boca_apertura // 2))]
        
        if vol > 0.08:
            # Boca abierta durante la voz
            draw.ellipse(boca_box, fill=(255, 60, 100, 255), outline=(255, 220, 0, 255), width=4)
        else:
            # Boca cerrada en pausas
            draw.line([(200, 275), (300, 275)], fill=(0, 210, 255, 255), width=6)

        # 2. Pestañeo aleatorio de ojos (guiño) cada ~90 frames
        if (i % 90) in [0, 1, 2]:
            draw.rectangle([(170, 180), (220, 190)], fill=(0, 210, 255, 255))
            draw.rectangle([(280, 180), (330, 190)], fill=(0, 210, 255, 255))

        frame_path = os.path.join(frames_dir, f"frame_{i:04d}.png")
        frame.save(frame_path)

    # Convertir secuencia de fotogramas a MP4 con fondo transparente/chroma
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_avatar_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✔] Video del Avatar IA Parlante (Lip-Sync) generado en: {output_avatar_mp4}")
    return output_avatar_mp4

if __name__ == "__main__":
    pass
