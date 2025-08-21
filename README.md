# AI-Powered-Financial-Fraud-Prevention
This project is an AI-powered fraud detection system designed to prevent financial fraud in online transactions. It uses machine learning algorithms to analyze transaction patterns and classify them as legitimate or fraudulent. The system is integrated with a web-based dashboard to visualize transactions, track fraud alerts, and monitor suspicious activities in real-time.

🚀 Features

✅ Detects fraudulent transactions using AI/ML models

✅ SQLite database (transactions.db) to store transaction history

✅ Interactive dashboard for visualizing fraud statistics

✅ Configurable environment using .env for deployment

✅ Ready-to-deploy on Replit / Local Server / Cloud

🧠 Algorithm / Working

Data Input: Transactions are fed into the system from the database (transactions.db).

Feature Extraction: Important attributes like amount, location, time, and transaction frequency are extracted.

Fraud Detection Model:

Machine learning algorithms (e.g., Logistic Regression / Random Forest / Decision Trees) are applied.

Model learns from historical data to classify transactions as Fraudulent (1) or Legitimate (0).

Prediction: When a new transaction occurs, the model predicts whether it is fraudulent.

Visualization: The results are displayed on the dashboard (transaction_dashboard.jpeg).

⚙️ Tech Stack

Python (core logic & ML model)

Flask / Streamlit (for web dashboard – runs via app.py)

SQLite (transactions.db) for data storage

Matplotlib / Seaborn (for data visualization)

Replit / Localhost (for deployment & testing)

🖥️ How to Run

Clone Repository

git clone https://github.com/your-username/Financial_Fraud_Prevention_AI.git
cd Financial_Fraud_Prevention_AI/MysteryMinds


Install Dependencies

pip install -r requirements.txt


Run Application

python app.py


or (if using main.py)

python main.py


Access Dashboard
Open browser → http://127.0.0.1:5000

📊 Output Example

Transactions flagged as suspicious will be highlighted.

Dashboard provides fraud statistics and visual insights.

Example screenshot:

📌 Use Cases

Online banking fraud prevention

Credit/debit card fraud detection

E-commerce transaction monitoring
