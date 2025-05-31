import numpy as np
import tensorflow as tf
import os


# 📍 Ruta al modelo y al directorio de prueba
modelo_path = '/model/modelo.h5'
test_dir = '/Dataset/data/arrays_np'

# 📦 Cargar modelo entrenado
model = tf.keras.models.load_model(modelo_path)

# 🔎 Buscar todos los archivos que comiencen por "GRABACION" y terminen en .npy
test_files = [f for f in os.listdir(test_dir) if f.startswith("grabacion") and f.endswith(".npy")]

print(f"🔍 {len(test_files)} archivos encontrados para inferencia.")

# 🧪 Procesar cada archivo
for file in test_files:
    path = os.path.join(test_dir, file)
    try:
        X = np.load(path)

        if X.shape != (30, 128, 128, 1):
            print(f"⚠️ {file} tiene forma incorrecta: {X.shape}")
            continue

        X = X / 255.0
        X = np.expand_dims(X, axis=0)  # Añadir batch

        pred = model.predict(X)
        pred_class = np.argmax(pred)

        print(f"📁 {file} → Clase predicha: {pred_class}")

    except Exception as e:
        print(f"❌ Error con {file}: {e}")