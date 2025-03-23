import os
import subprocess
import json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from rag_qa import query_rag  # Import QA function from rag_qa.py

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#  Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#  Function to Check Allowed File Type
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

#  Function to Run a Python Script
def run_script(script_name):
    try:
        print(f"🔹 Running {script_name}...")
        result = subprocess.run(["python", script_name], capture_output=True, text=True, check=True)
        print(f"✅ {script_name} executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:\n{e.stderr}")

#  Home Route - File Upload
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if a file is uploaded
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]

        # Check if the file is valid
        if file.filename == "" or not allowed_file(file.filename):
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        #  Save file as "cleaned_hotel_bookings.csv" to be used in processing
        df = pd.read_csv(file_path)
        df.to_csv("cleaned_hotel_bookings.csv", index=False)

        #  Run the Processing Pipeline
        scripts = ["data_preprocessing.py", "analytics.py", "faiss_index.py"]
        for script in scripts:
            run_script(script)

        #  Start API in the Background
        print("🚀 Starting API in the background...")
        try:
            subprocess.Popen(["python", "api.py"])  # Runs API in background
        except Exception as e:
            print(f"❌ Failed to start API: {e}")

        return redirect(url_for("home"))  # Redirect to analytics & QA page

    return render_template("upload.html")

#  Analytics & QA Page
@app.route("/home", methods=["GET", "POST"])
def home():
    answer = None
    curl_response = {}  # Ensure curl_response is always a dictionary

    if request.method == "POST":
        question = request.form["question"]
        answer = query_rag(question)  # Call QA function

        #  Execute cURL command to fetch API response
        curl_cmd = f'curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d "{{\\"question\\": \\"{question}\\"}}"'
        try:
            result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
            if result.stdout:  # Ensure there's output
                curl_response = json.loads(result.stdout)
            else:
                curl_response = {"error": "Empty response from API"}
        except Exception as e:
            curl_response = {"error": str(e)}

    return render_template("index.html", question=request.form.get("question", ""), answer=answer, curl_response=curl_response)

if __name__ == "__main__":
    app.run(debug=True)
