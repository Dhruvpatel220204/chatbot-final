WhatsEase — Fully fixed package (Flask backend + React frontend)

Structure:
- backend/   -> Flask app (SQLite) (run on http://127.0.0.1:5000)
- frontend/  -> React app (Parcel dev server) (run on http://localhost:3000)

Quick start:

1) Backend
cd backend
python -m venv venv
# activate venv:
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
# Backend will run on http://127.0.0.1:5000

2) Frontend (in separate terminal)
cd frontend
npm install
npm start
# Frontend dev server runs at http://localhost:3000

3) Use the app:
- Open http://localhost:3000
- Signup -> Login -> Inbox -> Chat with bot (__bot__@whatsease)
