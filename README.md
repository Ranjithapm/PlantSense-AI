
# PlantSense-AI 🌿

PlantSense-AI is a real-time agricultural intelligence system that uses Deep Learning and Visible-Range Multispectral Image Analysis to detect plant leaf diseases.

Developed under the research paper **“Deep Learning-Based Plant Stress Detection Using Leaf Image Analysis”**, the system combines CNN-based disease prediction with vegetation index analysis for accurate and reliable crop monitoring.

## 🚀 Features

* Real-time plant disease detection using leaf images
* Intelligent foliage validation using HSV masking
* MobileNetV2-based deep learning classifier
* Visible-light vegetation analysis using:

  * Excess Green (ExG)
  * Excess Red (ExR)
  * VARI
  * Greenness Percentage
* Actionable treatment recommendations
* Responsive React frontend with Flask backend

## 🧠 Deep Learning Model

The system uses a fine-tuned **MobileNetV2** model with transfer learning.

### Training Strategy

* **Phase 1:** Feature extraction with frozen base layers
* **Phase 2:** Fine-tuning top layers using low learning rate and callbacks such as:

  * EarlyStopping
  * ReduceLROnPlateau

## 🌱 Supported Crops & Diseases

### Pepper

* Bacterial Spot
* Healthy

### Potato

* Early Blight
* Late Blight
* Healthy

### Tomato

* Bacterial Spot
* Early Blight
* Late Blight
* Leaf Mold
* Septoria Leaf Spot
* Spider Mites
* Target Spot
* Yellow Leaf Curl Virus
* Mosaic Virus
* Healthy

## 🛠️ Tech Stack

### Frontend

* React 19
* Vite
* Axios

### Backend

* Flask REST API
* TensorFlow / Keras

## 📂 Project Structure

* `app.py` – Backend API
* `train_model.py` – Model training
* `frontend/` – React frontend
* `model/` – Trained model weights
* `class_indices.json` – Class mappings

## ▶️ Setup Instructions

### Backend

```bash
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📄 Research Details

**Paper Title:** Deep Learning-Based Plant Stress Detection Using Leaf Image Analysis

**Author:**
Ranjitha Prabha P

**Institution:**
Department of Computer Science and Engineering
St. Joseph’s Institute of Technology, Chennai, India
