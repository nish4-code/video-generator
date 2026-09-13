import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from voice_generator import generar_audio
from video_assembler import crear_video_short

def cargar_fuente(size=40):
    """
    Intenta cargar fuentes TrueType comunes en sistemas Debian/Ubuntu.
    Si no encuentra ninguna, recurre a la fuente por defecto.
    """
    posibles_fuentes = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for font_path in posibles_fuentes:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def superponer_tarjeta_y_texto(
    imagen_input_path: str,
    titulo: str,
    texto_guion: str,
    output_path: str = "assets/frame_con_texto.jpg"
) -> str:
    """
    Superpone una tarjeta semitransparente con título y texto formateado sobre la imagen de fondo.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if os.path.exists(imagen_input_path):
        img = Image.open(imagen_input_path).convert("RGBA")
        img = img.resize((1080, 1920))
    else:
        # Fondo degradado de seguridad si no existe la imagen
        print("[*] Creando fondo degradado oscuro de seguridad...")
        img = Image.new("RGBA", (1080, 1920), (15, 20, 32, 255))

    # Capa para tarjeta semitransparente (estilo Glassmorphism)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    # Dibujar contenedor central con borde neón
    card_box = [(90, 420), (990, 1500)]
    draw_overlay.rectangle(card_box, fill=(10, 14, 28, 220), outline=(0, 210, 255, 255), width=6)

    # Fusionar capas
    img_comp = Image.alpha_composite(img, overlay).convert("RGB")
    draw = ImageDraw.Draw(img_comp)

    font_titulo = cargar_fuente(54)
    font_cuerpo = cargar_fuente(36)

    # Dibujar Título principal en amarillo neón
    draw.text((540, 500), titulo, fill=(255, 220, 0), font=font_titulo, anchor="mm")
    
    # Línea decorativa
    draw.line([(180, 560), (900, 560)], fill=(0, 210, 255), width=4)

    # Ajustar líneas de texto del guion
    lineas = textwrap.wrap(texto_guion, width=32)
    y_text = 630
    for linea in lineas:
        draw.text((540, y_text), linea, fill=(245, 248, 255), font=font_cuerpo, anchor="mm")
        y_text += 55

    img_comp.save(output_path, quality=95)
    print(f"[✔] Imagen final con texto generada en: {output_path}")
    return output_path

def ejecutar_pipeline():
    """
    Orquesta el flujo completo: generación de voz, diseño visual con texto y ensamble de video.
    """
    titulo = "⚡ DATOS TECNOLÓGICOS ⚡"
    guion = (
        "Tres datos tecnológicos que probablemente no conocías. "
        "Número uno: El primer disco duro de cinco megabytes pesaba más de una tonelada. "
        "Número dos: Más del noventa por ciento del dinero del mundo existe solo en formato digital."
    )
    
    bg_image = "assets/sample_image.jpg"
    frame_image = "assets/frame_con_texto.jpg"
    audio_file = "assets/speech.wav"
    video_file = "short_demo.mp4"
    
    # 1. Generar la tarjeta de texto sobre la imagen de fondo
    superponer_tarjeta_y_texto(imagen_input_path=bg_image, titulo=titulo, texto_guion=guion, output_path=frame_image)
    
    # 2. Generar el audio sintético en español
    generar_audio(texto=guion, output_path=audio_file)
    
    # 3. Ensamblar el video final
    crear_video_short(imagen_path=frame_image, audio_path=audio_file, output_path=video_file)
    
    print("\n==========================================")
    print(f"¡Proceso completado! Video final: {video_file}")
    print("==========================================\n")

if __name__ == "__main__":
    ejecutar_pipeline()
