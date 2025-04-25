import os
import subprocess
from tkinter import filedialog, Tk

# Selección de archivo
Tk().withdraw()
video_path = filedialog.askopenfilename(title="Selecciona el video .mp4")

if not video_path:
    print("❌ No se seleccionó ningún archivo.")
    exit()
video_basename = os.path.splitext(os.path.basename(video_path))[0]

# Carpeta base del dataset
base_folder = os.path.join(os.path.dirname(video_path), "dataset")
os.makedirs(base_folder, exist_ok=True)

# Función para obtener duración
def get_duration(path):
    result = subprocess.run(
        [
            r"C:\Users\Raul\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path
        ],
        capture_output=True,
        text=True
    )
    return float(result.stdout.strip())

duration = get_duration(video_path)
fragment_duration = 2
total_fragments = int(duration // fragment_duration)

for index in range(total_fragments):
    start = index * fragment_duration
    numero = (index % 10) + 1  # Cíclico: 1 al 10

    # Crear carpeta para el número si no existe
    class_folder = os.path.join(base_folder, str(numero))
    os.makedirs(class_folder, exist_ok=True)

    # Guardar con nombre que incluya el número y el índice general
    output_path = os.path.join(class_folder, f"{video_basename}_{numero}_{index:04d}.mp4")

    subprocess.run([
        r"C:\Users\Raul\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe",
        "-ss", str(start),
        "-t", str(fragment_duration),
        "-i", video_path,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "slow",
        "-c:a", "aac",
        "-y",
        output_path
    ])

print("✅ Fragmentos creados y clasificados correctamente.")
print(f"📂 Dataset generado en: {base_folder}")
