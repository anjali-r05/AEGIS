AEGIS — AI-Powered Women’s Safety Intelligence Platform

AEGIS is a modern women’s safety and emergency response platform that provides rapid assistance during unsafe situations through one-tap SOS activation, live location sharing, trusted contact alerts, incident reporting, and real-time situational awareness.

The platform is built with a secure, scalable, and mobile-first architecture to support fast emergency response and proactive personal safety.

---

Key Features

- 🚨 One-tap SOS emergency activation
- 📍 Live location tracking and sharing
- 📲 Emergency contact notifications
- 📝 Incident reporting with detailed descriptions
- 📊 Real-time safety monitoring dashboard
- 📱 Fully responsive mobile-first interface
- 🔒 Secure and lightweight Flask-based backend

---

Tech Stack

Layer| Technology
Backend| Python, Flask
Frontend| HTML5, CSS3, JavaScript
Deployment| Google Cloud Run
Version Control| Git & GitHub

---

Project Structure

AEGIS/
├── app.py
├── templates/
├── static/
├── requirements.txt
├── Procfile
├── .gitignore
├── .env.example
└── README.md

---

Live Demo

🔗 Cloud Run Deployment:
https://ais-dev-64mwl3boicfzpz2j4thndb-694648297863.asia-southeast1.run.app/

---

Installation

git clone https://github.com/anjali-r05/AEGIS.git
cd AEGIS
pip install -r requirements.txt
python app.py

---

Environment Variables

Create a ".env" file in the project root and configure the required variables:

SECRET_KEY=your_secret_key_here
GOOGLE_API_KEY=your_google_api_key_here
FLASK_ENV=production
PORT=5000

---

Deployment

The application is production-ready and can be deployed on:

- Google Cloud Run
- Render
- Railway
- Any platform supporting Python + Gunicorn

Start Command

gunicorn app:app

---

Vision

AEGIS aims to become a reliable digital safety companion by combining AI capabilities, real-time communication, and emergency response workflows to improve personal safety awareness and enable faster assistance during critical situations.

---

Author

Anjali Rout

- B.Tech, Computer Science & Engineering (GGSIPU)
- Aspiring Software Development Engineer (SDE)
- Java Full Stack & AI Enthusiast

---

License

This project is currently maintained as a personal/hackathon project. All rights reserved by the author unless a separate open-source license is added in the future.
