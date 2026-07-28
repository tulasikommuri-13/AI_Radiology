# 🩻 AI Radiology Platform

An AI-powered web application for automated chest X-ray analysis using Deep Learning. The system predicts whether a chest X-ray indicates **Normal** or **Pneumonia**, displays the confidence score, stores patient records, and generates downloadable PDF medical reports.

---

## 🚀 Features

- 🧠 AI-based chest X-ray classification
- 📤 Upload chest X-ray images
- 👤 Patient information management
- 📊 Confidence score prediction
- 📄 Automatic PDF report generation
- 💾 SQLite database integration
- 🖥️ Responsive modern user interface
- 📂 Stores uploaded images and generated reports

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Flask

### AI / Machine Learning
- TensorFlow
- NumPy
- Pillow

### Database
- SQLite

### Report Generation
- ReportLab

---

## 📁 Project Structure

```
AI_Radiology/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── database.db
│
├── model/
│   └── pneumonia_model.h5
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── images/
│
├── templates/
│   └── index.html
│
├── uploads/
│
├── reports/
│
└── utils/
    └── preprocess.py
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/tulasikommuri-13/AI_Radiology.git
```

Move into the project

```bash
cd AI_Radiology
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

## 📷 Workflow

1. Enter patient details.
2. Upload a chest X-ray image.
3. AI analyzes the image.
4. Displays prediction and confidence score.
5. Generates a downloadable PDF report.
6. Stores patient information in the SQLite database.

---

## 📌 Future Improvements

- Multi-disease detection
- User authentication
- Cloud deployment
- Doctor dashboard
- Email report sharing
- DICOM image support

---

## 📄 License

This project is developed for educational and research purposes.
