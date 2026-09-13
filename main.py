import os
from voice_generator import generar_audio
from script_parser import parsear_guion_en_escenas
from stock_fetcher import obtener_clips_para_escenas
from subtitles_generator import generar_subtitulos_karaoke_ass
from avatar_overlay import generar_avatar_animado
from video_engine import ensamblar_video_multiescena, obtener_duracion_audio

def ejecutar_pipeline_v2():
    """
    Orquesta la Versión 2.0 del Generador de Videos Cortos:
    1. División del guion en multiescenas.
    2. Descarga / Generación de clips de video MP4 en movimiento por escena.
    3. Síntesis de voz natural con Kokoro-TTS.
    4. Generación de subtítulos dinámicos estilo Karaoke (Alex Hormozi / TikTok).
    5. Creación del avatar de personaje animado superpuesto.
    6. Ensamble final de video vertical en 1080x1920 con 44.1kHz estéreo.
    """
    print("\n============================================================")
    print("      GENERADOR DE VIDEOS CORTOS DE ALTA RETENCIÓN v2.0      ")
    print("============================================================\n")

    guion = (
        "Tres datos tecnológicos que probablemente no conocías. "
        "Número uno: El primer disco duro de cinco megabytes pesaba más de una tonelada. "
        "Número dos: Más del noventa por ciento del dinero del mundo existe solo en formato digital."
    )

    audio_file = "assets/speech.wav"
    ass_file = "assets/subtitles.ass"
    output_video = "short_v2_demo.mp4"

    # 1. Parsear el guion en escenas
    print("[1/6] Parseando guion en escenas cortas...")
    escenas = parsear_guion_en_escenas(guion)

    # 2. Generar el audio sintético en español
    print("[2/6] Sintetizando locución con Kokoro-TTS...")
    generar_audio(texto=guion, output_path=audio_file)
    duracion_total = obtener_duracion_audio(audio_file)

    # 3. Obtener clips de video en movimiento para cada escena
    print("[3/6] Obteniendo clips de video MP4 en movimiento...")
    clips_mp4 = obtener_clips_para_escenas(escenas)

    # 4. Generar subtítulos Karaoke estilo TikTok (Word-by-Word)
    print("[4/6] Generando subtítulos animados Karaoke ASS...")
    generar_subtitulos_karaoke_ass(texto_guion=guion, duracion_total=duracion_total, output_ass_path=ass_file)

    # 5. Generar avatar / personaje animado
    print("[5/6] Preparando personaje animado superpuesto...")
    avatar_png = generar_avatar_animado()

    # 6. Ensamblar el video final multiescena
    print("[6/6] Renderizando video final de alta retención...")
    ensamblar_video_multiescena(
        clips_mp4=clips_mp4,
        audio_voz_path=audio_file,
        subtitulos_ass_path=ass_file,
        avatar_png_path=avatar_png,
        output_video_path=output_video
    )

    print("\n============================================================")
    print(f" ¡Éxito! Video v2.0 generado en: {output_video}")
    print("============================================================\n")

if __name__ == "__main__":
    ejecutar_pipeline_v2()
