# NewsBuddy--Smart-personalized-News-Delivery-System
NewsBuddy is a mobile-friendly Streamlit web application that delivers country-wise and category-wise news with a smart fallback mechanism.
It is designed as a student project / internship project focusing on API integration, UI design, and deployment.

🚀 Features

🌍 Country-wise news selection

🏙️ Optional city-based news (smart fallback)

🗂️ Category-wise filtering

Business

Entertainment

General

Health

Science

Sports

Technology

🔁 Smart fallback logic

If city news not available → country news shown

📱 Mobile-friendly UI

🔊 Listen button ready (Text-to-Speech extensible)

☁️ Deployable on Streamlit Cloud

🛠️ Tech Stack

Frontend / UI: Streamlit

Backend: Python

API: NewsAPI

HTTP Requests: requests library

📁 Project Structure
NewsBuddy/
├── ui_app.py          # Streamlit UI
├── news_fetcher.py    # News fetching & fallback logic
├── requirements.txt  # Project dependencies
├── README.md         # Project documentation

📦 Requirements

Install dependencies using:

pip install -r requirements.txt


requirements.txt

streamlit
requests

▶️ How to Run Locally
streamlit run ui_app.py


Then open in browser:

http://localhost:8501

🔐 API Key Setup (IMPORTANT)

This project uses NewsAPI.

1️⃣ Get API Key

Visit: https://newsapi.org/

Sign up and get your API key

2️⃣ Set API Key (Recommended Way)

Do NOT hardcode API key

import os
API_KEY = os.getenv("NEWS_API_KEY")


For Streamlit Cloud, add in Secrets:

NEWS_API_KEY = "your_api_key_here"

🌍 Public Deployment (Recommended)

This project can be deployed using Streamlit Cloud (FREE):

Connect GitHub repository

Select ui_app.py as main file

Add API key in Secrets

Get a public URL (mobile + desktop supported)

🎯 Use Case

Academic / Internship project

Learning API integration

Streamlit UI development

Personalized news delivery system

📌 Future Enhancements

Text-to-Speech (TTS) full integration

User login & preferences

News summarization using NLP

Multilingual support

Mobile app using Flutter (API-based)

👨‍💻 Author

Himanshu Vaidya
Student | Data Science / AI / ML
Project: NewsBuddy – Smart Personalized News Delivery System
