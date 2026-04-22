# 🌿 PlantSense AI — Model Training Script
# Run this entire notebook in Google Colab (GPU runtime recommended)
# File: train_model.py  →  copy each cell into a Colab notebook

# ═══════════════════════════════════════════════════════════════════
# CELL 1 — Install & Import
# ═══════════════════════════════════════════════════════════════════
!pip install -q kaggle

import os, zipfile, shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt

print("TensorFlow version:", tf.__version__)
print("GPU available:", tf.config.list_physical_devices('GPU'))

# ═══════════════════════════════════════════════════════════════════
# CELL 2 — Download PlantVillage Dataset from Kaggle
# ═══════════════════════════════════════════════════════════════════
# Option A: Upload kaggle.json first, then run:
from google.colab import files
files.upload()   # upload your kaggle.json here

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d emmarex/plantdisease -p /content/dataset
with zipfile.ZipFile('/content/dataset/plantdisease.zip', 'r') as z:
    z.extractall('/content/dataset')

DATA_DIR = '/content/dataset/PlantVillage'
print("Classes found:", len(os.listdir(DATA_DIR)))

# ═══════════════════════════════════════════════════════════════════
# CELL 3 — Data Generators with Multispectral Augmentation
# ═══════════════════════════════════════════════════════════════════
IMG_SIZE   = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES= 15

train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=30,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],   # simulates lighting variation
    fill_mode='nearest',
)

train_gen = train_datagen.flow_from_directory(
    DATA_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='training', seed=42,
)
val_gen = train_datagen.flow_from_directory(
    DATA_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='validation', seed=42,
)

print("Train samples:", train_gen.samples)
print("Val samples  :", val_gen.samples)
print("Class indices:", train_gen.class_indices)

# ═══════════════════════════════════════════════════════════════════
# CELL 4 — Build MobileNetV2 Transfer Learning Model
# ═══════════════════════════════════════════════════════════════════
base_model = MobileNetV2(
    input_shape=(*IMG_SIZE, 3),
    include_top=False,
    weights='imagenet',
)
base_model.trainable = False   # freeze base initially

inputs  = tf.keras.Input(shape=(*IMG_SIZE, 3))
x       = base_model(inputs, training=False)
x       = layers.GlobalAveragePooling2D()(x)
x       = layers.Dense(256, activation='relu')(x)
x       = layers.Dropout(0.5)(x)
outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)

model = models.Model(inputs, outputs)
model.summary()

# ═══════════════════════════════════════════════════════════════════
# CELL 5 — Phase 1: Train Classification Head (5 epochs)
# ═══════════════════════════════════════════════════════════════════
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy'],
)

history1 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=5,
    callbacks=[EarlyStopping(patience=3, restore_best_weights=True)],
)

# ═══════════════════════════════════════════════════════════════════
# CELL 6 — Phase 2: Fine-tune Top 30 Layers of Base Model
# ═══════════════════════════════════════════════════════════════════
base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy'],
)

callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
    ModelCheckpoint('plant_model_best.h5', save_best_only=True, monitor='val_accuracy'),
    ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3, min_lr=1e-6),
]

history2 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=25,
    callbacks=callbacks,
)

# ═══════════════════════════════════════════════════════════════════
# CELL 7 — Evaluate & Plot
# ═══════════════════════════════════════════════════════════════════
val_gen_eval = ImageDataGenerator(rescale=1./255, validation_split=0.2).flow_from_directory(
    DATA_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='validation', seed=42, shuffle=False,
)
loss, acc = model.evaluate(val_gen_eval)
print(f"\n✅ Final Validation Accuracy: {acc*100:.2f}%")
print(f"✅ Final Validation Loss:     {loss:.4f}")

# Plot accuracy curve
all_acc = history1.history['accuracy'] + history2.history['accuracy']
all_val = history1.history['val_accuracy'] + history2.history['val_accuracy']
plt.figure(figsize=(10,4))
plt.plot(all_acc, label='Train Accuracy')
plt.plot(all_val, label='Val Accuracy')
plt.axvline(x=len(history1.history['accuracy'])-1, color='gray', linestyle='--', label='Fine-tune start')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.tight_layout()
plt.savefig('accuracy_plot.png', dpi=150)
plt.show()

# ═══════════════════════════════════════════════════════════════════
# CELL 8 — Save Model & Download
# ═══════════════════════════════════════════════════════════════════
model.save('plant_model.h5')
print("Model saved as plant_model.h5")

# Download to your computer
from google.colab import files
files.download('plant_model.h5')
files.download('accuracy_plot.png')

# ═══════════════════════════════════════════════════════════════════
# AFTER TRAINING:
# 1. Download plant_model.h5 from Colab
# 2. Create a folder called "model" inside your project directory
# 3. Place plant_model.h5 inside the "model" folder
# 4. Restart the Flask app — it will automatically load the real model
# ═══════════════════════════════════════════════════════════════════
