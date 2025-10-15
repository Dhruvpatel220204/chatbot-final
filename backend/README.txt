Backend (Flask + SQLite)

Run:
cd backend
python -m venv venv
# activate venv
# windows: venv\Scripts\activate
# mac/linux: source venv/bin/activate
pip install -r requirements.txt
python app.py

API:
POST /api/auth/signup  {email,password,display_name}
POST /api/auth/login   {email,password} -> returns access_token
GET /api/users (auth)
POST /api/messages (auth) {recipient,content}
GET /api/messages?with=<other> (auth)
