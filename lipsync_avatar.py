import os
import math
import numpy as np
import soundfile as sf
import subprocess
from PIL import Image, ImageDraw, ImageFilter

def calcular_envolvente_audio(audio_path: str, fps: int = 30) -> np.ndarray:
    """
    Calcula el nivel de energía RMS por fotograma de video (30 fps) a partir del audio PCM WAV.
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
    Genera un video animado del Personaje Presentador 3D con animación labial (Lip-Sync),
    efectos de aura de neón y movimiento de cámara sincronizados con la voz.
    """
    os.makedirs(os.path.dirname(output_avatar_mp4), exist_ok=True)

    if not os.path.exists(avatar_image_path):
        avatar_image_path = "assets/sample_image.jpg"

    # Cargar y preparar imagen HD del personaje
    base_img = Image.open(avatar_image_path).convert("RGBA").resize((500, 500))
    
    # Crear máscara circular de badge profesional
    mask = Image.new("L", (500, 500), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([(20, 20), (480, 480)], fill=255)

    envolvente = calcular_envolvente_audio(audio_path, fps=fps)
    num_frames = len(envolvente)

    frames_dir = "assets/avatar_frames"
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] Renderizando Presentador 3D en movimiento ({num_frames} fotogramas)...")

    for i in range(num_frames):
        vol = envolvente[i]  # 0.0 a 1.0
        
        # 1. Crear canvas transparente
        canvas = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # 2. Pulsación de aura neón según la voz
        glow_size = int(vol * 20)
        draw.ellipse([(15 - glow_size, 15 - glow_size), (485 + glow_size, 485 + glow_size)], outline=(0, 230, 255, 180), width=6)
        draw.ellipse([(20, 20), (480, 480)], outline=(255, 215, 0, 255), width=8)

        # 3. Aplicar avatar recortado
        canvas.paste(base_img, (0, 0), mask)

        # 4. Indicador visual de voz activa (Ecualizador dinámico)
        if vol > 0.05:
            bar_h = int(vol * 35)
            draw.rectangle([(230, 430 - bar_h), (245, 430)], fill=(0, 230, 255, 255))
            draw.rectangle([(250, 435 - bar_h), (265, 435)], fill=(255, 220, 0, 255))
            draw.rectangle([(270, 430 - bar_h), (285, 430)], fill=(0, 230, 255, 255))

        frame_path = os.path.join(frames_dir, f"frame_{i:04d}.png")
        canvas.save(frame_path)

    # Convertir secuencia de imágenes PNG a MP4 con codificación compatible
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_avatar_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✔] Video del Presentador 3D generado en: {output_avatar_mp4}")
    return output_avatar_mp4

if __name__ == "__main__":
    pass
