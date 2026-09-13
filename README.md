# Generador de Videos Cortos v3.0 (Avatar IA Parlante & Lip-Sync)

Sistema automatizado de producción de **videos verticales (9:16 - 1080x1920)** optimizado para **TikTok, YouTube Shorts e Instagram Reels**:

1. **Voz Nítida 1D Mono**: Síntesis de voz limpia sin garabatos ni distorsión resampleada a 44.1 kHz estéreo AAC.
2. **Avatar IA Parlante con Lip-Sync**: Personaje animado que abre y cierra la boca, guiña los ojos y se mueve en sincronía exacta con el volumen del audio.
3. **Clips en Movimiento por Escena (`.mp4`)**: Cambio continuo de tomas de fondo.
4. **Subtítulos Dinámicos Karaoke (TikTok / Alex Hormozi)**: Palabras iluminadas en amarillo neón exactamente en el segundo que se pronuncian.

---

## 1. Requisitos e Instalación en Debian

### Paso 1: Dependencias del Sistema
```bash
sudo apt update && sudo apt install -y \
    ffmpeg \
    python3 \
    python3-pip \
    python3-venv \
    libsndfile1 \
    espeak-ng
```

### Paso 2: Entorno Virtual e Instalación de Librerías Python
```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Ejecución

Con el entorno virtual activado (`source venv/bin/activate`):

```bash
python3 main.py
```

El resultado final se guardará en **`short_v3_demo.mp4`**.

---

## 3. Personalizar tu Propio Personaje / Avatar

Para colocar la foto de cualquier personaje o caricatura:
Reemplaza la imagen en **`assets/avatar/character.png`** por la imagen cuadrada (PNG) de tu personaje. El motor animará automáticamente la boca y rostro del personaje sobre la voz sintetizada.
