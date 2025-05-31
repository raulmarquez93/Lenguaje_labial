import cv2
import os
from tqdm import tqdm

# Ruta a los vídeos que quieres procesar
# video_dir = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/aumentado"
video_dir = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/prueba/convertidos_mp4"

# Ruta donde guardarás los frames extraídos
# output_dir = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/frames_extraidos"
output_dir = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/prueba/frames_extraidos_inferencia"


os.makedirs(output_dir, exist_ok=True)

# Recorremos todos los vídeos
for root, _, files in os.walk(video_dir):
    for file in tqdm(files):
        if not file.endswith(".mp4"):
            continue

        video_path = os.path.join(root, file)
        video_name = os.path.splitext(file)[0]
        save_path = os.path.join(output_dir, video_name)
        os.makedirs(save_path, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        frame_idx = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_filename = os.path.join(save_path, f"frame_{frame_idx:04d}.png")
            cv2.imwrite(frame_filename, frame)
            frame_idx += 1

        cap.release()
