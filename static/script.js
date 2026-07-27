const uploadForm = document.getElementById("uploadForm");
const previewImage = document.getElementById("previewImage");
const loading = document.getElementById("loading");
const resultCard = document.getElementById("resultCard");
const predictionText = document.getElementById("predictionText");
const confidenceText = document.getElementById("confidenceText");

const fileInput = document.querySelector("input[name='file']");

// ==========================
// IMAGE PREVIEW
// ==========================

fileInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (e) {

        previewImage.src = e.target.result;
        previewImage.style.display = "block";

    };

    reader.readAsDataURL(file);

});

// ==========================
// FORM SUBMIT
// ==========================

uploadForm.addEventListener("submit", async function (e) {

    e.preventDefault();

    loading.style.display = "block";
    resultCard.style.display = "none";

    const formData = new FormData(uploadForm);

    try {

        const response = await fetch("/predict", {

            method: "POST",
            body: formData

        });

        const data = await response.json();

        loading.style.display = "none";

        if (data.error) {

            alert(data.error);
            return;

        }

        resultCard.style.display = "block";
        document.getElementById("resultImage").src = previewImage.src;
        predictionText.innerHTML =
        "Diagnosis : <span style='color:#00c6ff'>" +
        data.prediction +
        "</span>";

        confidenceText.innerHTML =
        data.confidence + "%";

        if (data.prediction === "Normal") {

            predictionText.style.color = "#00ff88";

        } else {

            predictionText.style.color = "#ff4b4b";

        }

        resultCard.scrollIntoView({

            behavior: "smooth"

        });

    }

    catch (err) {

        loading.style.display = "none";

        alert("Server Error");

        console.log(err);

    }

});

// ==========================
// DOWNLOAD REPORT
// ==========================

function downloadPDF() {

    window.location.href = "/download-report";

}

// ==========================
// ANALYZE AGAIN
// ==========================

function resetForm() {

    uploadForm.reset();

    previewImage.style.display = "none";

    previewImage.src = "";

    resultCard.style.display = "none";

}

// ==========================
// FAQ
// ==========================

document.querySelectorAll(".faq-item").forEach(item => {

    item.addEventListener("click", () => {

        item.classList.toggle("active");

    });

});

// ==========================
// MOBILE MENU
// ==========================

const menuBtn = document.querySelector(".menu-btn");

const navLinks = document.querySelector(".nav-links");

if (menuBtn) {

    menuBtn.addEventListener("click", () => {

        if (navLinks.style.display === "flex") {

            navLinks.style.display = "none";

        }

        else {

            navLinks.style.display = "flex";
            navLinks.style.flexDirection = "column";

        }

    });

}

// ==========================
// SMOOTH SCROLL
// ==========================

document.querySelectorAll("a[href^='#']").forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
        .scrollIntoView({

            behavior: "smooth"

        });

    });

});

async function loadHistory(){

    const response = await fetch("/history");

    const data = await response.json();

    const container = document.getElementById("historyContainer");

    container.innerHTML = "";

    data.forEach(patient=>{

        container.innerHTML += `

        <div class="history-card">

            <img src="${patient.image}">

            <h3>${patient.name}</h3>

            <p><b>Prediction:</b> ${patient.prediction}</p>

            <p><b>Confidence:</b> ${patient.confidence}%</p>

            <p>${patient.date}</p>

            <button
            class="delete-btn"
            onclick="deletePatient(${patient.id})">

            Delete

            </button>

        </div>

        `;

    });

}

loadHistory();

async function deletePatient(id){

    await fetch("/delete/"+id,{

        method:"DELETE"

    });

    loadHistory();

}