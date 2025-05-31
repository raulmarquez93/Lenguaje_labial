import cv2
import albumentations as A
import os
from tqdm import tqdm
import numpy as np

# Usamos ReplayCompose para aplicar la MISMA transformación a todos los frames
transform = A.ReplayCompose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=10, p=0.5),
    A.GaussianBlur(p=0.2),
    A.MotionBlur(p=0.2),
    A.RandomGamma(p=0.3),
    A.ImageCompression(quality_lower=75, quality_upper=100, p=0.3)
])

def augment_video_consistently(video_path, output_dir, augment_count=5):
    cap = cv2.VideoCapture(video_path)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    if len(frames) == 0:
        return  # Saltar vídeos vacíos

    filename = os.path.splitext(os.path.basename(video_path))[0]
    height, width = frames[0].shape[:2]

    for i in range(augment_count):
        # Generar transformación fija para este vídeo
        example_aug = transform(image=frames[0])
        replay = example_aug["replay"]

        out_path = os.path.join(output_dir, f"{filename}_aug{i+1}.mp4")
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (width, height))

        for frame in frames:
            aug_frame = A.ReplayCompose.replay(replay, image=frame)["image"]
            out.write(aug_frame)
        out.release()

def process_dataset(root_dir, output_root, augment_count=5):
    for dirpath, _, filenames in os.walk(root_dir):
        for file in tqdm(filenames):
            if file.endswith(".mp4"):
                video_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(dirpath, root_dir)
                out_dir = os.path.join(output_root, rel_path)
                os.makedirs(out_dir, exist_ok=True)
                augment_video_consistently(video_path, out_dir, augment_count)

# 🏁 Ejecutar
# input_dataset = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/convertidos_mp4/dataset"
# output_dataset = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/aumentado"
input_dataset = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/inferencia/convertidos_mp4/dataset"
output_dataset = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/inferencia/aumentado"
process_dataset(input_dataset, output_dataset, augment_count=5)
