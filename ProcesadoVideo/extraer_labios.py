import os
import cv2
import numpy as np
from tqdm import tqdm
import mediapipe as mp

# Configuración
input_dir = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/prueba/frames_extraidos_inferencia"
output_dir = "C:/Users/Raul/Documentos/GitHub/Lenguaje_labial/Dataset/data/inferencia_np"
frame_size = 128  # Subido a 128 para más calidad
num_frames = 30

# Inicializar MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    refine_landmarks=True,
    max_num_faces=1,
    min_detection_confidence=0.5
)

# Tus puntos buenos de la boca
lip_ids = sorted(list(set([
    # Labios exteriores
    61, 185, 40, 39, 37, 0, 267, 269, 270, 409,
    291, 375, 321, 405, 314, 17, 84, 181, 91, 146,
    # Labios interiores
    78, 191, 80, 81, 82, 13, 312, 311, 310, 415,
    308, 324, 318, 402, 317, 14, 87, 178, 88, 95
])))

# Función para extraer la boca recortada
def get_lip_crop(image):
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_face_landmarks:
        h, w, _ = image.shape
        landmarks = results.multi_face_landmarks[0].landmark
        lip_points = [landmarks[i] for i in lip_ids]

        xs = [int(point.x * w) for point in lip_points]
        ys = [int(point.y * h) for point in lip_points]

        padding = 10  # Mejorado el padding
        x_min = max(min(xs) - padding, 0)
        x_max = min(max(xs) + padding, w)
        y_min = max(min(ys) - padding, 0)
        y_max = min(max(ys) + padding, h)

        if x_max - x_min <= 0 or y_max - y_min <= 0:
            return None  # Protección si falla el recorte

        crop = image[y_min:y_max, x_min:x_max]
        crop = cv2.resize(crop, (frame_size, frame_size), interpolation=cv2.INTER_AREA)  # Redimensionar bien
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)  # Luego pasar a grises

        return crop
    else:
        return None

# Procesar una carpeta de frames
def process_video_folder(folder_path, output_path):
    try:

        frame_files = sorted(os.listdir(folder_path))
        frames = []

        for file in frame_files:
            if not file.endswith(".png"):
                continue
            img_path = os.path.join(folder_path, file)
            image = cv2.imread(img_path)
            if image is None:
                print(f"❌ Imagen no leída correctamente: {img_path}")
                continue
            crop = get_lip_crop(image)
            if crop is not None:
                frames.append(crop)

        if len(frames) == 0:
            print(f"⚠️ No se detectaron labios en: {folder_path}")
            return

        # Uniformar a num_frames
        if len(frames) >= num_frames:
            frames = frames[:num_frames]
        else:
            while len(frames) < num_frames:
                frames.append(frames[-1])

        # Convertir a numpy array: (frames, height, width, 1)
        frames_np = np.stack(frames, axis=0).astype(np.uint8)
        frames_np = np.expand_dims(frames_np, axis=-1)

        np.save(output_path, frames_np)
    except Exception as e:
        print(f"💥 Error procesando {folder_path}: {e}")

# Procesar todas las carpetas
os.makedirs(output_dir, exist_ok=True)
print("🔄 Procesando vídeos...")



from tqdm import tqdm
import sys

folders = [f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))]
for folder_name in tqdm(folders, desc="Procesando", ascii=True, file=sys.stdout):
    folder_path = os.path.join(input_dir, folder_name)
    if not os.path.isdir(folder_path):
        print("❌ No es un directorio, se omite.")
        continue
    output_path = os.path.join(output_dir, f"{folder_name}.npy")
    print(f" Procesando carpeta: {folder_name}")
    process_video_folder(folder_path, output_path)


face_mesh.close()
