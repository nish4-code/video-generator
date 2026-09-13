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
    Garantiza la conversión de segmentos multidimensionales a un vector 1D continuo
    para evitar distorsión o garabateo de audio.
    """
    print(f"[*] Sintetizando voz con Kokoro-TTS (Voz: {voice}, Idioma: {lang_code})...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pipeline = KPipeline(lang_code=lang_code)
    generator = pipeline(texto, voice=voice, speed=1.0, split_pattern=r'\n+')
    
    audio_segments = []
    for _, _, audio in generator:
        if audio is not None:
            # Convertir PyTorch tensor a NumPy si es necesario
            if hasattr(audio, "numpy"):
                audio = audio.numpy()
            # Aplanar a vector 1D de float32
            audio_flat = np.asarray(audio, dtype=np.float32).flatten()
            if len(audio_flat) > 0:
                audio_segments.append(audio_flat)
        
    if not audio_segments:
        raise ValueError("No se pudo generar el audio a partir del texto proporcionado.")
        
    # Concatenar a lo largo del eje 0 para formar un stream mono nítido
    final_audio = np.concatenate(audio_segments, axis=0)
    sf.write(output_path, final_audio, 24000)
    
    print(f"[✔] Audio limpio NÍTIDO guardado exitosamente en: {output_path}")
    return output_path

if __name__ == "__main__":
    texto_prueba = (
        "¿Sabías que el primer procesador comercial de la historia, el Intel 4004, "
        "tenía una velocidad de reloj de apenas 740 kilohercios? Hoy, tu teléfono es millones de veces más rápido."
    )
    generar_audio(texto_prueba)
