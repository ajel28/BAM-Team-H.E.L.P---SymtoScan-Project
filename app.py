import logging
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ai import getResponse
from secret import *

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    chat_data = db.Column(db.JSON, nullable=False, default=[])

with app.app_context():
    db.create_all()

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/diagnose', methods=["GET", "POST"])
def diagnose():
    username = session.get('username', 'Guest')
    return render_template('diagnose.html', username=username)

@app.route('/SymptoScan')
def SymptScan():
    return render_template('SymptoScan.html')

@app.route('/symrelief')
def symrelief():
    return render_template('symrelief.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(name=username).first()

        if user is None:
            return render_template('login.html', error=f"This username ({username}) doesn't exist. Please try again.")
        else:
            if user.password == password:
                session['username'] = user.name
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error="Incorrect password. Please try again.")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        userName = request.form.get('name')
        pwd = request.form.get('password')
        email = request.form.get('email')

        emailExists = User.query.filter_by(email=email).first()
        userNameExists = User.query.filter_by(name=userName).first()

        if emailExists:
            return render_template('signup.html', error=f"This email ({email}) already exists.")
        elif userNameExists:
            return render_template('signup.html', error=f"This username ({userName}) already exists.")
        elif len(pwd) < 5:
            return render_template('signup.html', error="Your password is too short. It must be at least 8 characters long.")
        else:
            newUser = User(name=userName, email=email, password=pwd)
            db.session.add(newUser)
            db.session.commit()

        session['username'] = userName
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_input = data.get('prompt', '')

    logging.debug(f"Received user input: {user_input}")

    try:
        if 'chat_state' not in session:
            session['chat_state'] = {"step": "start"}

        chat_state = session['chat_state']
        ai_response, new_state = getResponse(chat_state, user_input)

        session['chat_state'] = new_state

        logging.debug(f"AI response: {ai_response}")

        return jsonify({'response': ai_response})
    except Exception as e:
        logging.error(f"Error during get_response: {e}")
        return jsonify({'response': 'Error: Unable to get response from server.'}), 500

@app.route('/end_chat', methods=['POST'])
def end_chat():
    session.pop('chat_state', None)
    return jsonify({'message': 'Chat ended'})


@app.route('/Navigation')
def Navagation():
    return render_template('Navigation.html')

if __name__ == '__main__':
    app.run(debug=True)