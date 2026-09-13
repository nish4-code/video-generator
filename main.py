import os
from voice_generator import generar_audio
from script_parser import parsear_guion_en_escenas
from stock_fetcher import obtener_clips_para_escenas
from subtitles_generator import generar_subtitulos_karaoke_ass
from lipsync_avatar import generar_video_avatar_lipsync
from video_engine import ensamblar_video_multiescena, obtener_duracion_audio

def ejecutar_pipeline_v3():
    """
    Orquesta la Versión 3.0 del Generador de Videos Cortos:
    1. División del guion en multiescenas.
    2. Síntesis de voz limpia NÍTIDA 1D (Kokoro-TTS).
    3. Descarga / Generación de clips MP4 en movimiento por escena.
    4. Generación del Avatar IA Parlante en movimiento sincronizado (Lip-Sync).
    5. Subtítulos Karaoke estilo TikTok (Word-by-Word).
    6. Ensamble de video vertical 1080x1920 con audio 44.1kHz estéreo.
    """
    print("\n============================================================")
    print("      GENERADOR DE VIDEOS CORTOS v3.0 (AVATAR LIP-SYNC)     ")
    print("============================================================\n")

    guion = (
        "Tres datos tecnológicos que probablemente no conocías. "
        "Número uno: El primer disco duro de cinco megabytes pesaba más de una tonelada. "
        "Número dos: Más del noventa por ciento del dinero del mundo existe solo en formato digital."
    )

    audio_file = "assets/speech.wav"
    ass_file = "assets/subtitles.ass"
    avatar_video = "assets/talking_avatar.mp4"
    output_video = "short_v3_demo.mp4"

    # 1. Parsear guion en escenas
    print("[1/6] Parseando guion en escenas cortas...")
    escenas = parsear_guion_en_escenas(guion)

    # 2. Generar audio sintético limpio 1D sin distorsión
    print("[2/6] Sintetizando voz NÍTIDA con Kokoro-TTS...")
    generar_audio(texto=guion, output_path=audio_file)
    duracion_total = obtener_duracion_audio(audio_file)

    # 3. Clips de movimiento para el fondo por escena
    print("[3/6] Obteniendo clips de fondo MP4 en movimiento...")
    clips_mp4 = obtener_clips_para_escenas(escenas)

    # 4. Generar Avatar IA Parlante con sincronización labial (Lip-Sync)
    print("[4/6] Generando video de Avatar IA Parlante con Lip-Sync...")
    generar_video_avatar_lipsync(audio_path=audio_file, output_avatar_mp4=avatar_video)

    # 5. Generar Subtítulos Karaoke ASS estilo TikTok
    print("[5/6] Generando subtítulos Karaoke animados ASS...")
    generar_subtitulos_karaoke_ass(texto_guion=guion, duracion_total=duracion_total, output_ass_path=ass_file)

    # 6. Ensamblar todo en el video final
    print("[6/6] Renderizando video final v3.0...")
    ensamblar_video_multiescena(
        clips_mp4=clips_mp4,
        audio_voz_path=audio_file,
        subtitulos_ass_path=ass_file,
        talking_avatar_mp4=avatar_video,
        output_video_path=output_video
    )

    print("\n============================================================")
    print(f" ¡Éxito! Video v3.0 generado en: {output_video}")
    print("============================================================\n")

if __name__ == "__main__":
    ejecutar_pipeline_v3()
