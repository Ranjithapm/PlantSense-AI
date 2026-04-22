# PlantSense-AI


# AI-Powered Grievance Redressal Portal 🏛️🤖

An intelligent, full-stack, omnichannel grievance management system designed to streamline the process of filing, categorizing, routing, and resolving citizen complaints. This platform leverages modern web technologies and advanced Artificial Intelligence (NLP, Computer Vision, and Speech-to-Text) to automate workflows and ensure timely resolution.

## 🌟 Key Features

*   **Omnichannel Intake:** Citizens can file grievances via web forms, document uploads, or voice notes.
*   **Regional Language Support:** Built-in support for Tamil voice complaints using **AssemblyAI** for Speech-to-Text and **Google Translate API** for English translation.
*   **AI-Powered Categorization & Routing:** Automatically classifies the grievance category (e.g., Water, Roads, Sanitation) and routes it to the correct department using **Google Gemini AI**.
*   **Intelligent Entity Extraction:** Uses a local Python **SpaCy NER** (Named Entity Recognition) model to extract crucial details like location, jurisdiction, and area from complaint text.
*   **Document & Image Processing:** Extracts text from uploaded documents using **Tesseract.js (OCR)** and utilizes **YOLOv8** for image-based problem detection (e.g., identifying potholes or garbage dumps).
*   **Role-Based Access Control (RBAC):** Dedicated dashboards and interfaces for Citizens, Authorities/Officers, and System Admins.
*   **Automated SLA Tracking:** Automatically assigns Service Level Agreement (SLA) deadlines (e.g., 21 days) and tracks the status lifecycle from "Registered" to "Closed".
*   **Analytics & Dashboard:** Interactive visual dashboards for authorities and admins to monitor grievance trends, resolution rates, and pending tasks.

---

## 💻 Tech Stack

### Frontend
*   **React.js** (Bootstrapped with Vite for fast builds)
*   **React Router DOM** (Client-side routing)
*   **Chart.js / react-chartjs-2** (Interactive data visualization and analytics)
*   **Axios** (API requests)
*   **Lucide React** (Modern iconography)

### Backend
*   **Node.js & Express.js** (RESTful API architecture)
*   **MongoDB & Mongoose** (NoSQL Database for flexible schema management)
*   **JWT & Bcrypt** (Secure authentication and password hashing)
*   **Multer** (Handling file and audio uploads)

### Artificial Intelligence & Machine Learning
*   **Google Gemini API:** Core LLM for intelligent text processing and decision-making.
*   **AssemblyAI:** Highly accurate Speech-to-Text engine for processing voice notes.
*   **Google Translate API:** For breaking language barriers (Tamil to English).
*   **Python & SpaCy:** Local Machine Learning scripts for Custom Named Entity Recognition (NER).
*   **Tesseract.js:** Optical Character Recognition (OCR) to read text from citizen-uploaded images/documents.
*   **YOLOv8 (PyTorch):** Computer vision model for object detection in uploaded evidence photos.

---

## 🏗️ Project Architecture

1.  **Client Tier:** React frontend interacts with the citizen or officer.
2.  **API Gateway:** Express.js handles incoming HTTP requests, file uploads, and authentication.
3.  **AI Processing Pipeline:** 
    *   *Voice Input* -> AssemblyAI -> Google Translate -> NLP processing.
    *   *Image Input* -> YOLOv8 / Tesseract.js -> Context extraction.
    *   *Text Input* -> Spacy NER & Gemini -> Classification & Routing.
4.  **Data Tier:** MongoDB stores User profiles, Grievance tickets, Audit logs, and Action Taken Reports (ATRs).

---

## 🚀 Getting Started

### Prerequisites
*   Node.js (v18+)
*   Python 3.8+ (for SpaCy NER and YOLOv8 models)
*   MongoDB (Local or Atlas)
*   API Keys needed: Google Gemini, AssemblyAI, Google Translate.

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/AI_GrievancePortal.git
cd AI_GrievancePortal

**2. Setup Backend**
cd backend
npm install
# Create a .env file based on .env.example and add your API keys/Database URI
npm run dev

**3. Setup Frontend**
cd ../frontend
npm install
npm run dev

**4. Setup Local Python AI Models**
Ensure Python is installed and install the required ML packages:
pip install spacy ultralytics
python -m spacy download en_core_web_sm
