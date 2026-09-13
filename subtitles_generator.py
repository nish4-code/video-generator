import os
import re
from typing import List, Dict

def generar_subtitulos_karaoke_ass(
    texto_guion: str,
    duracion_total: float,
    output_ass_path: str = "assets/subtitles.ass"
) -> str:
    """
    Genera un archivo de subtítulos .ASS con formato Karaoke estilizado (TikTok / Alex Hormozi),
    fuente destacada en amarillo neón con caja de fondo y contorno negro de alta legibilidad.
    """
    os.makedirs(os.path.dirname(output_ass_path), exist_ok=True)
    
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hormozi, Arial, 64, &H00FFFFFF, &H0000FFFF, &H00000000, &HAA000000, 1, 0, 0, 0, 100, 100, 0, 0, 1, 5, 2, 2, 60, 60, 750, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    palabras = texto_guion.split()
    total_palabras = len(palabras)
    if total_palabras == 0:
        return output_ass_path

    tiempo_por_palabra = duracion_total / total_palabras
    
    # Grupos de 3 palabras para lectura de alto impacto
    bloques = []
    tamano_bloque = 3
    for i in range(0, total_palabras, tamano_bloque):
        bloques.append(palabras[i:i + tamano_bloque])

    eventos = []
    tiempo_actual = 0.0

    for idx, grupo in enumerate(bloques):
        duracion_grupo = len(grupo) * tiempo_por_palabra
        t_inicio = tiempo_actual
        t_fin = t_inicio + duracion_grupo
        tiempo_actual = t_fin

        def fmt_time(s: float) -> str:
            hrs = int(s // 3600)
            mins = int((s % 3600) // 60)
            secs = int(s % 60)
            cs = int((s - int(s)) * 100)
            return f"{hrs}:{mins:02d}:{secs:02d}.{cs:02d}"

        str_inicio = fmt_time(t_inicio)
        str_fin = fmt_time(t_fin)

        palabras_formateadas = []
        for p_idx, word in enumerate(grupo):
            word_clean = re.sub(r'[^\wáéíóúÁÉÍÓÚñÑ]', '', word).upper()
            if p_idx == 0:
                palabras_formateadas.append(r"{\c&H00D7FF&\b1}" + word_clean + r"{\r}")
            else:
                palabras_formateadas.append(r"{\c&H00FFFFFF&}" + word_clean)

        linea_texto = " ".join(palabras_formateadas)
        eventos.append(f"Dialogue: 0,{str_inicio},{str_fin},Hormozi,,0,0,0,,{linea_texto}")

    contenido_final = ass_header + "\n".join(eventos) + "\n"

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(contenido_final)

    print(f"[✔] Subtítulos Karaoke ASS legibles generados en: {output_ass_path}")
    return output_ass_path

if __name__ == "__main__":
    pass
