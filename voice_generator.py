import os
import soundfile as sf
import numpy as np
from kokoro import KPipeline

def generar_audio(
    texto: str,
    output_path: str = "assets/speech.wav",
    lang_code: str = "e",
    voice: str = "em_alex"
) -> str:
    """
    Sintetiza audio a partir de texto utilizando Kokoro-TTS.
    
    Parámetros:
        texto (str): Texto en español a sintetizar.
        output_path (str): Ruta donde se guardará el archivo audio WAV.
        lang_code (str): Código de idioma ('e' para español / es).
        voice (str): Voz deseada (ej. 'em_alex', 'em_santa', 'ef_dora').
        
    Retorna:
        str: Ruta del archivo generado.
    """
    print(f"[*] Sintetizando voz con Kokoro-TTS (Voz: {voice}, Idioma: {lang_code})...")
    
    # Asegurar que el directorio de salida exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pipeline = KPipeline(lang_code=lang_code)
    generator = pipeline(texto, voice=voice, speed=1.0, split_pattern=r'\n+')
    
    audio_segments = []
    for _, _, audio in generator:
        audio_segments.append(audio)
        
    if not audio_segments:
        raise ValueError("No se pudo generar el audio a partir del texto proporcionado.")
        
    final_audio = np.concatenate(audio_segments)
    sf.write(output_path, final_audio, 24000)
    
    print(f"[✔] Audio guardado exitosamente en: {output_path}")
    return output_path

if __name__ == "__main__":
    texto_prueba = (
        "¿Sabías que el primer procesador comercial de la historia, el Intel 4004, "
        "tenía una velocidad de reloj de apenas 740 kilohercios? Hoy, tu teléfono es millones de veces más rápido."
    )
    generar_audio(texto_prueba)
