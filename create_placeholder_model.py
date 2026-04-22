import tensorflow as tf
import os

print("Generating a placeholder model perfectly shaped for app.py (15 classes)...")

# Create a small, untrained model that accepts (224, 224, 3) and outputs 15 classes
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(224, 224, 3)),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(15, activation='softmax')
])

# Save the model
os.makedirs('model', exist_ok=True)
model_path = os.path.join('model', 'plant_model.h5')
model.save(model_path)

print(f"Success! Un-trained placeholder model saved to {model_path}.")
