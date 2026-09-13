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
    talking_avatar_mp4: str,
    output_video_path: str = "short_v3_demo.mp4"
) -> str:
    """
    Ensambla escenas de fondo HD en movimiento, superpone el Presentador 3D con halo de neón
    y aplica los subtítulos Karaoke estilo TikTok en 1080x1920 con audio 44.1kHz estéreo.
    """
    duracion_audio = obtener_duracion_audio(audio_voz_path)

    print(f"[*] Ensamblando video multiescena con Presentador 3D (Duración: {duracion_audio:.2f}s)...")

    concat_txt_path = "assets/clips_list.txt"
    os.makedirs(os.path.dirname(concat_txt_path), exist_ok=True)
    with open(concat_txt_path, "w") as f:
        for clip in clips_mp4:
            clip_abs = os.path.abspath(clip)
            f.write(f"file '{clip_abs}'\n")

    # Filtro complejo de FFmpeg:
    # 0: Fondo multiescena -> Escalar a 1080x1920
    # 1: Audio PCM de voz sintetizada NÍTIDA
    # 2: Presentador 3D -> Escalar a 360x360 y superponer al centro inferior (x=360, y=1180)
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[bg];"
        f"[2:v]scale=360:360[avatar];"
        f"[bg][avatar]overlay=x=360:y=1180[video_avatar];"
        f"[video_avatar]subtitles='{subtitulos_ass_path}'[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt_path,
        "-i", audio_voz_path,
        "-i", talking_avatar_mp4,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-t", str(duracion_audio + 0.2),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-movflags", "+faststart",
        output_video_path
    ]

    subprocess.run(cmd, check=True)
    print(f"[✔] Video final v3.0 HD exportado exitosamente en: {output_video_path}")
    return output_video_path

if __name__ == "__main__":
    pass
