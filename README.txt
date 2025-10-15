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

4)Example try to chat with bot-

# Simple intents
INTENTS - 

•hi/hello/hey - "Hello! I'm •whatsapp chatbot AI . How can I help you?"
•how are you - "I'm a bot doing great!”
•help/support - Sure - tell me what you need help with.
•price/cost - "Prices depend on the item. Which item are you asking about?”
•thank/b - "You're welcome!”
•bye/goodbye - "Goodbye! Have a great day."

•DEFAULT_REPLY = "Sorry, I didn't understand that. Can you rephrase?*
