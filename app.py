from flask import Flask, render_template, redirect, url_for, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/diagnose')
def diagnose():
    return render_template('diagnose.html')

@app.route('/SymptoScan')
def SymptScan():
    return render_template('SymptoScan.html')

@app.route('/symrelief')
def symrelief():
    return render_template('symrelief.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Replace with your database query logic
        # Example assumes User model has 'name' and 'password' fields
        user = User.query.filter_by(name=username).first()

        if user is None:
            error_message = f"This username ({username}) doesn't exist. Please try again."
            return render_template('login.html', error=error_message)
        else:
            if user.password == password:
                session['username'] = user.name  # Store the username in the session
                return redirect(url_for('index'))
            else:
                error_message = "Incorrect password. Please try again."
                return render_template('login.html', error=error_message)

    return render_template('login.html')

@app.route('/', methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        userName = request.form.get('name')
        pwd = request.form.get('password')
        email = request.form.get('email')
        
        emailExsist = User.query.filter_by(email = email).first()
        userNameExsist = User.query.filter_by(name = userName).first()
        
        if emailExsist:
            error_message = f"This email ({email}) already exists."
            return render_template('signup.html', error=error_message)
        elif userNameExsist:
            error_message = f"This username ({userName}) already exists."
            return render_template('signup.html', error=error_message)
        elif len(pwd) < 5:
            error_message = "Your password is too short. It must be at least 8 characters long."
            return render_template('signup.html', error=error_message)
        else:
            newUser = User(name = userName, email = email, password = pwd)
            db.session.add(newUser)
            db.session.commit()
                  
        print(userName, pwd, email)
        session['username'] = userName  # Store the username in the session
        return redirect(url_for('home'))
    return render_template('signup.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
