from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt, os, uuid, re
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Config
SECRET_KEY = os.environ.get('SECRET_KEY', 'change_this_secret')
DB_URL = os.environ.get('DATABASE_URL', 'sqlite:///whats_ease.db')

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

# Database setup (SQLAlchemy)
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message_id = Column(String, unique=True, nullable=False)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='Sent')  # Sent, Delivered, Read
    is_bot_response = Column(Boolean, default=False)

class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Simple intents
INTENTS = [
    (re.compile(r'^(hi|hello|hey)\b', re.I), "Hello! I'm chatbot AI. How can I help you?"),
    (re.compile(r'how are you', re.I), "I'm a bot — doing great!"),
    (re.compile(r'help|support', re.I), "Sure — tell me what you need help with."),
    (re.compile(r'price|cost', re.I), "Prices depend on the item. Which item are you asking about?"),
    (re.compile(r'thank\b', re.I), "You're welcome!"),
    (re.compile(r'bye|goodbye', re.I), "Goodbye! Have a great day.")
]
DEFAULT_REPLY = "Sorry, I didn't understand that. Can you rephrase?"

def create_access_token(email, expires_minutes=60*24):
    payload = {'sub': email, 'exp': datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('sub')
    except Exception:
        return None

def log_activity(actor, action, details=''):
    a = Activity(actor=actor, action=action, details=details, timestamp=datetime.utcnow())
    db.add(a)
    db.commit()

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    display = data.get('display_name','')
    if not email or not password:
        return jsonify({'error':'email and password required'}), 400
    if db.query(User).filter_by(email=email).first():
        return jsonify({'error':'user exists'}), 400
    user = User(email=email, display_name=display, password_hash=generate_password_hash(password))
    db.add(user); db.commit()
    log_activity(email, 'signup', display)
    return jsonify({'message':'user created'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email'); password = data.get('password')
    if not email or not password:
        return jsonify({'error':'email and password required'}), 400
    user = db.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error':'invalid credentials'}), 401
    token = create_access_token(email)
    log_activity(email, 'login', '')
    return jsonify({'access_token': token, 'token_type':'bearer', 'email': email})

def auth_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization','')
        if not auth.startswith('Bearer '):
            return jsonify({'error':'missing token'}), 401
        token = auth.split(' ',1)[1]
        email = decode_token(token)
        if not email:
            return jsonify({'error':'invalid token'}), 401
        request.user = email
        return f(*args, **kwargs)
    return decorated

@app.route('/api/users', methods=['GET'])
@auth_required
def list_users():
    q = request.args.get('q','')
    query = db.query(User)
    if q:
        query = query.filter((User.email.contains(q)) | (User.display_name.contains(q)))
    users = [{'email':u.email,'display_name':u.display_name} for u in query.all()]
    return jsonify(users)

@app.route('/api/messages', methods=['POST'])
@auth_required
def create_message():
    data = request.json or {}
    sender = request.user
    recipient = data.get('recipient')
    content = data.get('content','').strip()
    if not recipient or not content:
        return jsonify({'error':'recipient and content required'}), 400
    message_id = uuid.uuid4().hex
    m = Message(message_id=message_id, sender=sender, recipient=recipient, content=content, timestamp=datetime.utcnow(), status='Sent', is_bot_response=False)
    db.add(m); db.commit()
    log_activity(sender, 'message_sent', f"to={recipient} id={message_id}")
    # Bot handling
    if recipient == '__bot__@whatsease':
        bot_reply = generate_bot_reply(sender, content)
        bot_id = uuid.uuid4().hex
        bm = Message(message_id=bot_id, sender='__bot__@whatsease', recipient=sender, content=bot_reply, timestamp=datetime.utcnow(), status='Sent', is_bot_response=True)
        db.add(bm); db.commit()
        log_activity('__bot__@whatsease','bot_replied', f"to={sender} id={bot_id}")
    return jsonify({'message_id': message_id}), 201

@app.route('/api/messages', methods=['GET'])
@auth_required
def list_messages():
    user = request.user
    other = request.args.get('with')
    if other:
        msgs = db.query(Message).filter(
            ((Message.sender==user)&(Message.recipient==other)) | ((Message.sender==other)&(Message.recipient==user))
        ).order_by(Message.timestamp).all()
    else:
        msgs = db.query(Message).filter((Message.sender==user)|(Message.recipient==user)).order_by(Message.timestamp).all()
    out = []
    for m in msgs:
        out.append({
            'message_id': m.message_id,
            'sender': m.sender,
            'recipient': m.recipient,
            'content': m.content,
            'timestamp': m.timestamp.isoformat(),
            'status': m.status,
            'is_bot_response': bool(m.is_bot_response)
        })
    return jsonify(out)

@app.route('/api/messages/<message_id>', methods=['PUT'])
@auth_required
def update_message(message_id):
    data = request.json or {}
    status = data.get('status')
    if status not in ('Sent','Delivered','Read'):
        return jsonify({'error':'invalid status'}), 400
    m = db.query(Message).filter_by(message_id=message_id).first()
    if not m:
        return jsonify({'error':'not found'}), 404
    m.status = status; db.commit()
    log_activity(request.user, 'message_status_updated', f"id={message_id} status={status}")
    return jsonify({'message':'updated'})

@app.route('/api/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    msg = db.query(Message).filter(Message.id == msg_id).first()
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    db.delete(msg)
    db.commit()
    return jsonify({'success': True})

@app.route('/api/activity', methods=['GET'])
@auth_required
def get_activity():
    acts = db.query(Activity).order_by(Activity.timestamp.desc()).limit(100).all()
    out = [{'actor':a.actor,'action':a.action,'details':a.details,'timestamp':a.timestamp.isoformat()} for a in acts]
    return jsonify(out)

def generate_bot_reply(user_email, message):
    print("User message:", message)  # Debug print
    text = message.lower()
    if "name" in text:
        print("Matched 'name' intent!")  # Debug print
        return "My name is Chatbot AI."
    for pattern, resp in INTENTS:
        if pattern.search(text):
            return resp
    return DEFAULT_REPLY

# Serve frontend build (if present)
@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
