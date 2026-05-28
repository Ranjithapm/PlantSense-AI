# PlantSense-AI

PlantSense-AI is a real-time agricultural intelligence system that integrates Deep Learning Classification with Visible-Range Multispectral Image Analysis to identify and diagnose crop leaf diseases.

Developed under your research paper "Deep Learning-Based Plant Stress Detection Using Leaf Image Analysis", it stands out from other classifiers by combining neural network diagnostics with deterministic botanical indicators and safety filters.

🚀 Key Technical Features
Intelligent Foliage Check (HSV Masking)

How it works: When a user uploads an image, the backend converts it to the HSV color space and isolates green hues (Hue: 35–85, Saturation/Value filters).
Why it's unique: It checks the greenness pixel ratio. If the image has less than 6% green pixels, the server rejects it. This acts as a robust filter against background noise, accidental uploads, and non-plant pictures.
Visible-Light Pseudo-Multispectral Telemetry

Computes vegetation indices straight from standard RGB camera uploads to provide objective health metrics alongside the "black-box" CNN predictions:
Excess Green (ExG): 2G−R−B — Measures crop canopy density and green vigor.
Excess Red (ExR): 1.4R−G — Highlights necrotic (dead/decayed) spots or dry tissue.
Visible Atmospherically Resistant Index (VARI):  
G+R−B
G−R
​
  — Normalizes ambient daylight and atmospheric fluctuations for reliable field photography.
Overall Greenness Percentage: Reflects chlorophyll levels.
Fine-Tuned MobileNetV2 Neural Network

Transfer Learning: Adapts the pre-trained ImageNet MobileNetV2 model to agricultural specifics.
Two-Phase Training Strategy (train_model.py):
Phase 1 (Feature Extraction): Freezes the base layers and trains the custom classification head (pooling, Dense 256, Dropout 50%, Softmax) for 5 epochs using a learning rate of 10 
−3
 .
Phase 2 (Fine-Tuning): Unfreezes the top 30 base layers and trains the network at a micro-learning rate of 10 
−4
  using dynamic callbacks like ReduceLROnPlateau and EarlyStopping to avoid overfitting.
Actionable Remediation Engine

Evaluates diagnostic states and returns targeted organic, physical, or chemical treatment plans for immediate crop care.
Premium Full-Stack Architecture

Frontend: Built with React 19, Vite, and Axios. Features a responsive floating-node canvas particle system (BgParticles.jsx), glassmorphic layouts, live drag-and-drop uploads, and rich progress indicators.
Backend: A Flask REST API (app.py) running on port 5001 that processes files, runs computer vision checks, and runs model predictions.
📂 Directory Architecture
A complete breakdown of your project's structure has been structured in the README, including:

Core Logic: app.py, train_model.py, class_indices.json
Automated Scripts: INSTALL_DEPENDENCIES.bat, START_PROJECT.bat (Windows master launchers)
Design Components: frontend/src/components/ (results visualizers, upload widgets, active canvas particles)
Model Storage: model/ directory for the plant_model.h5 weights.
📋 Supported Crop Directory (15-Class Palette)
Supports Tomato, Potato, and Pepper crops, covering:

Pepper: Bacterial Spot, Healthy
Potato: Early Blight, Late Blight, Healthy
Tomato: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites (Two-Spotted Spider Mite), Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy
🛠️ Quick Installation and Setup Instructions
Automated (Windows):
Double-click INSTALL_DEPENDENCIES.bat to automatically download Python requirements and setup React libraries.
Double-click START_PROJECT.bat to simultaneously run the Flask Server (http://localhost:5001) and the Vite React server (http://localhost:3000).
Manual Setup (Cross-Platform):
Backend: pip install -r requirements.txt followed by python app.py
Frontend: cd frontend, npm install, then npm run dev
📝 Academic Attribution
Your authors and department details have been fully integrated into the citations:

Paper Title: Deep Learning-Based Plant Stress Detection Using Leaf Image Analysis
Authors: Ranjitha Prabha P & Monisha J R
Institution: Department of Computer Science and Engineering, St. Joseph’s Institute of Technology, Chennai, India
What I Have Done:
Created and wrote a comprehensive, professionally styled, and technical markdown document to your 
README.md
.
Verified that it captures all specific equations (ExG, ExR, VARI), setup scripts, model architectures (two-phase MobileNetV2), folder layouts, and academic credits.
