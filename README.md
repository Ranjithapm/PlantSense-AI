# PlantSense-AI 🌿

PlantSense-AI is an AI-powered agricultural intelligence system designed for **early plant stress and disease detection using leaf image analysis**.

The system combines **deep learning-based disease classification** with **visible-light vegetation index analysis** to provide useful insights into plant health and support early crop monitoring.

## 🚀 Features

* 🌱 Real-time plant leaf disease detection
* 🔍 Leaf and foliage validation using HSV-based image processing
* 🧠 MobileNetV2-based deep learning classification
* 📊 Vegetation analysis using:

  * Excess Green (ExG)
  * Excess Red (ExR)
  * Visible Atmospherically Resistant Index (VARI)
  * Greenness Percentage
* 💡 Plant health insights and treatment recommendations
* 🖥️ Responsive React frontend
* ⚙️ Flask REST API backend

## 🧠 Deep Learning Model

PlantSense-AI uses **MobileNetV2 with transfer learning** for plant disease classification.

### Training Approach

The model is trained in two stages:

1. **Feature Extraction**

   * The base MobileNetV2 layers are frozen.
   * The newly added classification layers are trained.

2. **Fine-Tuning**

   * Selected layers of the pretrained model are unfrozen.
   * The model is fine-tuned using a low learning rate.
   * Training uses callbacks such as:

     * EarlyStopping
     * ReduceLROnPlateau

## 🌱 Supported Crops

The current model supports the following crops:

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

## 📊 Image Analysis

In addition to disease classification, PlantSense-AI analyzes visible characteristics of plant leaves using image-processing techniques.

The system calculates vegetation indices such as:

| Index       | Purpose                                            |
| ----------- | -------------------------------------------------- |
| ExG         | Estimates green vegetation intensity               |
| ExR         | Measures red-channel dominance                     |
| VARI        | Estimates vegetation from visible RGB information  |
| Greenness % | Provides an approximate measure of green leaf area |

These measurements can complement the deep learning prediction and provide additional information about plant condition.

## 🛠️ Technology Stack

### Frontend

* React 19
* Vite
* Axios

### Backend

* Python
* Flask
* TensorFlow
* Keras
* OpenCV

### Machine Learning

* MobileNetV2
* Transfer Learning
* Image Preprocessing
* Vegetation Index Analysis

## 📂 Project Structure

```text
PlantSense-AI/
│
├── app.py
├── train_model.py
├── requirements.txt
├── class_indices.json
│
├── model/
│   └── trained model files
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

## ▶️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Ranjithapm/PlantSense-AI.git
cd PlantSense-AI
```

### 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Flask Backend

```bash
python app.py
```

### 4. Install Frontend Dependencies

Open another terminal:

```bash
cd frontend
npm install
```

### 5. Start the React Frontend

```bash
npm run dev
```

The frontend can then be accessed through the local URL provided by Vite.

## 🔬 Research Details

**Paper Title:**
Deep Learning-Based Plant Stress Detection Using Leaf Image Analysis

**Author:**
Ranjitha Prabha P

**Institution:**
Department of Computer Science and Engineering
St. Joseph’s Institute of Technology
Chennai, India

## 🎯 Objective

The primary objective of PlantSense-AI is to combine **deep learning and image-based vegetation analysis** to support early identification of plant diseases and stress conditions.

The system is intended to provide a simple and accessible approach for analyzing plant health using leaf images.
