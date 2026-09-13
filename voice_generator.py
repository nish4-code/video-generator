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
    Normaliza la amplitud y exporta en formato estándar PCM 16-bit WAV (24000 Hz)
    para garantar reproducción cristalina en todos los reproductores de Linux.
    """
    print(f"[*] Sintetizando voz con Kokoro-TTS (Voz: {voice}, Idioma: {lang_code})...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pipeline = KPipeline(lang_code=lang_code)
    generator = pipeline(texto, voice=voice, speed=1.0, split_pattern=r'\n+')
    
    audio_segments = []
    for _, _, audio in generator:
        if audio is not None:
            if hasattr(audio, "numpy"):
                audio = audio.numpy()
            audio_flat = np.asarray(audio, dtype=np.float32).flatten()
            if len(audio_flat) > 0:
                audio_segments.append(audio_flat)
        
    if not audio_segments:
        raise ValueError("No se pudo generar el audio a partir del texto proporcionado.")
        
    final_audio = np.concatenate(audio_segments, axis=0)

    # 1. Normalizar amplitud al 95% de nivel máximo para evitar saturación o distorsión
    max_amp = np.max(np.abs(final_audio))
    if max_amp > 0:
        final_audio = (final_audio / max_amp) * 0.95

    # 2. Exportar explícitamente como PCM_16 bit WAV (compatibilidad 100% en Linux/Debian/Totem/VLC)
    sf.write(output_path, final_audio, 24000, subtype='PCM_16')
    
    print(f"[✔] Audio PCM-16 cristalino generado exitosamente en: {output_path}")
    return output_path

if __name__ == "__main__":
    texto_prueba = "Prueba de audio nítido en formato PCM 16 bits."
    generar_audio(texto_prueba)
