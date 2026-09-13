import os
import subprocess
from typing import List

def obtener_duracion_audio(audio_path: str) -> float:
    """
    Obtiene la duración exacta de un archivo audio con ffprobe.
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
    return float(res.stdout.strip())

def ensamblar_video_multiescena(
    clips_mp4: List[str],
    audio_voz_path: str,
    subtitulos_ass_path: str,
    avatar_png_path: str,
    output_video_path: str = "short_v2_demo.mp4"
) -> str:
    """
    Ensambla clips de video en movimiento por escena, incrusta el avatar en la esquina inferior,
    aplica subtítulos karaoke dinámicos y exporta el video en 1080x1920 44.1kHz estéreo.
    """
    duracion_audio = obtener_duracion_audio(audio_voz_path)
    duracion_escena = duracion_audio / len(clips_mp4) if clips_mp4 else duracion_audio

    print(f"[*] Ensamblando {len(clips_mp4)} escenas en movimiento (Duración: {duracion_audio:.2f}s)...")

    # Crear lista de concat para FFmpeg
    concat_txt_path = "assets/clips_list.txt"
    os.makedirs(os.path.dirname(concat_txt_path), exist_ok=True)
    with open(concat_txt_path, "w") as f:
        for clip in clips_mp4:
            clip_abs = os.path.abspath(clip)
            f.write(f"file '{clip_abs}'\n")

    # Filtro complejo para unir escenas, agregar avatar en movimiento y subtítulos karaoke
    # avatar superpuesto abajo al centro/derecha (overlay)
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[bg];"
        f"[2:v]scale=220:220[avatar];"
        f"[bg][avatar]overlay=x=780:y=1550[video_with_avatar];"
        f"[video_with_avatar]subtitles='{subtitulos_ass_path}'[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt_path,
        "-i", audio_voz_path,
        "-i", avatar_png_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-t", str(duracion_audio + 0.3),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        output_video_path
    ]

    subprocess.run(cmd, check=True)
    print(f"[✔] Video de Alta Retención exportado en: {output_video_path}")
    return output_video_path

if __name__ == "__main__":
    pass
