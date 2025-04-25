import os
import subprocess
from tkinter import filedialog, Tk

# Seleccionar carpeta
Tk().withdraw()
folder = filedialog.askdirectory(title="Selecciona la carpeta con los videos .webm")

if not folder:
    print("No se seleccionó ninguna carpeta.")
    exit()

# Crear carpeta de salida
output_folder = os.path.join(folder, "convertidos_mp4")
os.makedirs(output_folder, exist_ok=True)

# Procesar archivos
for file in os.listdir(folder):
    if file.lower().endswith(".webm"):
        input_path = os.path.join(folder, file)
        output_path = os.path.join(output_folder, file.replace(".webm", ".mp4"))
        print(f"Convirtiendo: {file} -> {os.path.basename(output_path)}")

        subprocess.run([
            r"C:\Users\Raul\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe",
            "-i", input_path,
            "-r", "30",                  # Fuerza framerate constante
            "-c:v", "libx264",
            "-crf", "16",                # 🔥 Alta calidad
            "-preset", "slow",           # 🔥 Mejor compresión
            "-c:a", "aac",
            "-movflags", "+faststart",
            output_path
        ])



print("\n✅ Conversión completada. Videos .mp4 guardados en:")
print(output_folder)
