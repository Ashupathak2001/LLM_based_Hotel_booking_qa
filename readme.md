# 📊 Hotel Booking QA System (RAG-based)

The **Hotel Booking QA System** is an AI-powered **Question-Answering (QA) System** that provides insights into hotel booking data.  
It allows users to **upload hotel booking CSV files**, ask **natural language questions**, and get **real-time analytics** using **FAISS-based Retrieval-Augmented Generation (RAG)**.

---

## 🚀 Features

✅ **Upload and analyze hotel booking CSV files**  
✅ **Ask natural language questions** (e.g., "Show me total revenue for July 2017")  
✅ **Real-time response & analytics using FAISS**  
✅ **Performance evaluation (API response time, FAISS retrieval speed)**  
✅ **Flask-based web UI & FastAPI backend for scalability**  

---

## 📂 Project Structure

hotel_booking_qa/ │── uploads/ # Directory for uploaded CSV files │── templates/ # HTML templates for the web app │ ├── index.html # Main UI for asking questions │ ├── upload.html # UI for uploading CSV files │── data_preprocessing.py # Cleans and prepares dataset │── analytics.py # Generates analytics & insights │── faiss_index.py # Embeds data & builds FAISS index │── rag_qa.py # Retrieves answers from FAISS │── api.py # FastAPI service for querying QA system │── app.py # Flask web application │── documents.pkl # Serialized text documents │── faiss_index.bin # FAISS vector index │── requirements.txt # List of dependencies │── README.md # Documentation (this file)


---

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/hotel_booking_qa.git
cd hotel_booking_qa

2️⃣ Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt
4️⃣ Run the Application
Step 1: Start the API

python api.py

Step 2: Start the Web App

python app.py
👉 Open http://127.0.0.1:5000/ in your browser.

📌 How to Use
Step 1: Upload a CSV File
Visit http://127.0.0.1:5000/

Click "Upload & Process" to analyze hotel bookings.

Step 2: Ask a Question
Enter a question (e.g., "Which locations had the highest booking cancellations?")

Click "Ask" to get an answer.

Step 3: View Results
The system retrieves relevant booking data and answers your question.

Performance metrics (API response time, FAISS retrieval speed) are displayed.

🌐 API Documentation
POST /ask
Request

{
  "question": "Which locations had the highest booking cancellations?"
}
Response

{
  "question": "Which locations had the highest booking cancellations?",
  "answer": "Based on retrieved data: Hotel A, Hotel B...",
  "response_time_ms": 120.5,
  "faiss_retrieval_time_ms": 50.3
}
📊 Performance Evaluation
Tracked Metrics
✅ API Response Time (response_time_ms)
✅ FAISS Retrieval Speed (faiss_retrieval_time_ms)

How It Works
API Response Time = Time taken to process the entire request.

FAISS Retrieval Time = Time taken to fetch the most relevant documents.

These metrics help optimize the system’s efficiency.

🛠️ Troubleshooting
Issue	Possible Fix
API response is empty	Restart api.py & app.py, ensure FAISS index exists
FAISS index not found	Run python faiss_index.py to generate the index
Slow response time	Reduce printing (print()) in api.py & rag_qa.py
Web app not loading	Ensure app.py is running & visit http://127.0.0.1:5000/
🤝 Contributing
Feel free to fork this repository and submit pull requests!
Issues & suggestions are welcome. 🚀

📜 License
This project is licensed under the MIT License.


---

### **📌 How to Use This `README.md`**
1️⃣ **Copy and save this file** as `README.md`.  
2️⃣ **Ensure your project follows the folder structure** mentioned above.  
3️⃣ **Modify the GitHub link** in the clone command if needed.  

🚀 **Now, your project is fully documented and ready for GitHub! Let me know if you need modifications.** 🚀
