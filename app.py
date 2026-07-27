from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from PIL import Image
import tensorflow as tf
import numpy as np
import sqlite3
import os
import uuid

app = Flask(__name__)

# ==========================================
# CREATE REQUIRED FOLDERS
# ==========================================

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

# ==========================================
# DATABASE
# ==========================================

def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,
        age INTEGER,
        phone TEXT,

        prediction TEXT,
        confidence REAL,

        image TEXT,
        report TEXT,

        date TEXT

    )
    """)

    conn.commit()
    conn.close()


init_db()

# ==========================================
# LOAD AI MODEL
# ==========================================

print("Loading AI Model...")

model = tf.keras.models.load_model("model/pneumonia_model.h5")

print("Model Loaded Successfully")

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")
# ==========================================
# AI PREDICTION
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        name = request.form.get("name")
        age = request.form.get("age")
        phone = request.form.get("phone")

        if not name or not age or not phone:
            return jsonify({"error": "Please fill all fields"})

        if "file" not in request.files:
            return jsonify({"error": "No image uploaded"})

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Please choose an image"})

        # ==========================================
        # SAVE IMAGE
        # ==========================================

        unique_name = str(uuid.uuid4()) + "_" + file.filename

        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_name
        )

        file.save(image_path)

        # ==========================================
        # IMAGE PREPROCESSING
        # ==========================================

        image = Image.open(image_path).convert("RGB")
        image = image.resize((224, 224))

        img = np.array(image) / 255.0
        img = np.expand_dims(img, axis=0)

        # ==========================================
        # MODEL PREDICTION
        # ==========================================

        prediction = model.predict(img)

        confidence = float(prediction[0][0])

        if confidence > 0.5:

            result = "Pneumonia"

        else:

            result = "Normal"

        confidence_percent = round(confidence * 100, 2)

        # ==========================================
        # PDF NAME
        # ==========================================

        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        pdf_name = f"{name}_{current_date}_Radiology_Report.pdf"

        pdf_path = os.path.join(
            app.config["REPORT_FOLDER"],
            pdf_name
        )

        # ==========================================
        # CREATE PDF
        # ==========================================

        c = canvas.Canvas(pdf_path, pagesize=letter)

        c.setFont("Helvetica-Bold", 20)
        c.drawString(140, 770, "AI RADIOLOGY REPORT")

        c.setFont("Helvetica", 12)

        c.drawString(50, 735, f"Date : {datetime.now()}")

        c.drawString(50, 715, f"Patient : {name}")

        c.drawString(50, 695, f"Age : {age}")

        c.drawString(50, 675, f"Phone : {phone}")

        c.setFont("Helvetica-Bold", 14)

        c.drawString(50, 635, "Diagnosis")

        if result == "Pneumonia":

            c.setFillColor(colors.red)

        else:

            c.setFillColor(colors.green)

        c.drawString(70, 610, result)

        c.setFillColor(colors.black)

        c.drawString(
            70,
            590,
            f"Confidence : {confidence_percent}%"
        )

        # ==========================================
        # X-RAY IMAGE IN PDF
        # ==========================================

        try:

            c.drawImage(
                image_path,
                300,
                430,
                width=220,
                height=220
            )

        except:

            pass

        c.setFont("Helvetica-Oblique", 10)

        c.drawString(
            50,
            80,
            "AI generated report. Doctor confirmation required."
        )

        c.save()
                # ==========================================
        # SAVE LAST REPORT
        # ==========================================

        app.config["LAST_REPORT"] = pdf_path

        # ==========================================
        # SAVE TO DATABASE
        # ==========================================

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO patients
        (
            name,
            age,
            phone,
            prediction,
            confidence,
            image,
            report,
            date
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            age,
            phone,
            result,
            confidence_percent,
            image_path,
            pdf_path,
            datetime.now().strftime("%d-%m-%Y %H:%M")
        ))

        conn.commit()
        conn.close()

        # ==========================================
        # RETURN RESULT TO WEBSITE
        # ==========================================

        return jsonify({

            "prediction": result,

            "confidence": confidence_percent

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500
    # ==========================================
# DOWNLOAD LATEST REPORT
# ==========================================
@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        "uploads",
        filename
    )
@app.route("/download-report")
def download_report():

    pdf_path = app.config.get("LAST_REPORT")

    if not pdf_path or not os.path.exists(pdf_path):

        return "No report available.", 404

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=os.path.basename(pdf_path)
    )


# ==========================================
# RECENT SCANS API
# ==========================================

@app.route("/history")
def history():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM patients
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    data = []

    for row in rows:

        data.append({

            "id": row["id"],
            "name": row["name"],
            "age": row["age"],
            "phone": row["phone"],
            "prediction": row["prediction"],
            "confidence": row["confidence"],
            "image": "/uploads/" + os.path.basename(row["image"]),
            "report": row["report"],
            "date": row["date"]

        })

    return jsonify(data)


# ==========================================
# DELETE SCAN
# ==========================================

@app.route("/delete/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT image, report FROM patients WHERE id=?",
        (patient_id,)
    )

    row = cursor.fetchone()

    if row:

        if row["image"] and os.path.exists(row["image"]):
            os.remove(row["image"])

        if row["report"] and os.path.exists(row["report"]):
            os.remove(row["report"])

        cursor.execute(
            "DELETE FROM patients WHERE id=?",
            (patient_id,)
        )

        conn.commit()

    conn.close()

    return jsonify({

        "message": "Record deleted successfully."

    })


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )