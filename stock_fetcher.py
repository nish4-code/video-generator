import os
import requests
import subprocess
from typing import List, Dict

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

def descargar_clip_pexels(keyword: str, output_path: str, duration_sec: int = 5) -> bool:
    """
    Intenta descargar un video vertical HD en movimiento desde la API de Pexels.
    """
    if not PEXELS_API_KEY:
        return False

    url = f"https://api.pexels.com/videos/search?query={keyword}&orientation=portrait&per_page=3"
    headers = {"Authorization": PEXELS_API_KEY}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            videos = data.get("videos", [])
            if videos:
                video_files = videos[0].get("video_files", [])
                for vf in video_files:
                    if vf.get("width", 0) < vf.get("height", 0) and vf.get("height", 0) >= 1080:
                        v_url = vf.get("link")
                        print(f"[*] Descargando clip HD de Pexels para '{keyword}'...")
                        v_res = requests.get(v_url, stream=True, timeout=15)
                        with open(output_path, "wb") as f:
                            for chunk in v_res.iter_content(chunk_size=1024*1024):
                                f.write(chunk)
                        return True
    except Exception as e:
        print(f"[!] Error conectando a Pexels API: {e}")

    return False

def generar_clip_animado_fallback(output_path: str, duration_sec: float = 4.0, bg_image: str = "assets/background.jpg"):
    """
    Genera un clip de video vertical MP4 (1080x1920) en movimiento HD utilizando
    el fondo Cyberpunk de alta definición con animación Ken Burns de cámara.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    frames = int(duration_sec * 30)

    if not os.path.exists(bg_image):
        bg_image = "assets/sample_image.jpg"

    # Animación fluida de zoom cámara sobre imagen HD
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", bg_image,
        "-filter_complex",
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0012,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30[v]",
        "-map", "[v]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", str(duration_sec),
        output_path
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✔] Clip HD animado generado en: {output_path}")

def obtener_clips_para_escenas(escenas: List[Dict[str, str]], base_dir: str = "assets/videos") -> List[str]:
    """
    Obtiene o genera los archivos de video MP4 en movimiento para cada escena del guion.
    """
    os.makedirs(base_dir, exist_ok=True)
    rutas_clips = []

    for esc in escenas:
        clip_path = os.path.join(base_dir, f"scene_{esc['id']}.mp4")
        
        # 1. Verificar si existe clip local preguardado
        if os.path.exists(clip_path):
            rutas_clips.append(clip_path)
            continue
            
        # 2. Intentar API Pexels
        exito = descargar_clip_pexels(esc["keyword"], clip_path)
        
        # 3. Si no hay API o falla, generar clip HD animado
        if not exito:
            generar_clip_animado_fallback(clip_path, duration_sec=4.0)

        rutas_clips.append(clip_path)

    return rutas_clips

if __name__ == "__main__":
    pass
