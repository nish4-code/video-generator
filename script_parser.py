import re
from typing import List, Dict

def parsear_guion_en_escenas(guion: str) -> List[Dict[str, str]]:
    """
    Divide un guion de texto en fragmentos de escena breves (~3-5 segundos por escena)
    y extrae palabras clave para la búsqueda de clips de video en movimiento.
    """
    # Limpiar y dividir por oraciones o comas principales
    oraciones = re.split(r'(?<=[.?!])\s+', guion.strip())
    escenas = []

    keywords_preset = [
        "technology cyber futuristic",
        "digital data network",
        "abstract neon background",
        "artificial intelligence computer"
    ]

    idx = 0
    for oracion in oraciones:
        if not oracion.strip():
            continue
            
        kw = keywords_preset[idx % len(keywords_preset)]
        escenas.append({
            "id": idx + 1,
            "texto": oracion.strip(),
            "keyword": kw
        })
        idx += 1

    return escenas

if __name__ == "__main__":
    ejemplo_guion = (
        "Tres datos tecnológicos que probablemente no conocías. "
        "Número uno: El primer disco duro de cinco megabytes pesaba más de una tonelada. "
        "Número dos: Más del noventa por ciento del dinero del mundo existe solo en formato digital."
    )
    resultado = parsear_guion_en_escenas(ejemplo_guion)
    print(f"Escenas detectadas ({len(resultado)}):")
    for esc in resultado:
        print(f" - Escena {esc['id']}: [{esc['keyword']}] -> \"{esc['texto']}\"")
