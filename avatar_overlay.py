import os
from PIL import Image, ImageDraw

def generar_avatar_animado(output_dir: str = "assets/avatar") -> str:
    """
    Genera un sprite o secuencia de imágen para el personaje animado parlante.
    Si ya existe un avatar personalizado en assets/avatar/character.png, lo reutiliza.
    """
    os.makedirs(output_dir, exist_ok=True)
    avatar_file = os.path.join(output_dir, "character.png")

    if not os.path.exists(avatar_file):
        print("[*] Generando sprite de personaje animado...")
        img = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Círculo base de personaje tipo robot/avatar
        draw.ellipse([(50, 50), (350, 350)], fill=(30, 144, 255, 240), outline=(0, 240, 255, 255), width=8)
        # Ojos fluorescentes
        draw.ellipse([(120, 130), (170, 180)], fill=(255, 255, 255, 255))
        draw.ellipse([(230, 130), (280, 180)], fill=(255, 255, 255, 255))
        draw.ellipse([(140, 145), (165, 170)], fill=(0, 210, 255, 255))
        draw.ellipse([(250, 145), (275, 170)], fill=(0, 210, 255, 255))
        # Boca en sonrisa parlante
        draw.arc([(130, 200), (270, 280)], start=0, end=180, fill=(255, 255, 255, 255), width=10)

        img.save(avatar_file)
        print(f"[✔] Sprite de avatar generado en: {avatar_file}")

    return avatar_file

if __name__ == "__main__":
    generar_avatar_animado()
