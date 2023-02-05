from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secretkey142857"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=21)

db = SQLAlchemy(app)

# Defining class for the users
class users(db.Model):
    id     = db.Column("id", db.Integer, primary_key=True)
    uname  = db.Column("uname", db.String(100))
    name   = db.Column("name", db.String(100))
    email  = db.Column("email", db.String(100))
    passwd = db.Column("passwd", db.String(60))

    def __init__(self, uname, name, email, passwd):
        self.uname  = uname
        self.name   = name
        self.email  = email
        self.passwd = passwd


# Routings start here
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        session["user"] = user

        found_user = users.query.filter_by(uname=users).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = users(user, " ")
            db.session.add(usr)
            db.commit()

        return redirect(url_for('user', usr=user))
    else: 
        if "user" in session:
            flash('Login Successful')
            return redirect(url_for('user', usr=session["user"]))

        return render_template('login.html', title='Login Page')

@app.route('/user', methods=['POST', 'GET'])
def user(usr):
    email = None
    if "user" in session: 
        usr = session["user"]

        if request.method == "POST":
            email = request.form['email']
            session['email'] = email
        else:
            if 'email' in session:
                email = session['email']

        return render_template('feed.html', email=email)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():    
    if "user" in session:
        user = session['user']
        flash(f"You have been logged out, {user}", 'info')
    
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        reg_email = request.form['email']

        if users.query.filter_by(email=reg_email).first():
            flash(f'An account using {reg_email} already exists.\n')

        reg_uname = request.form['uname']

        if users.query.filter_by(uname=reg_uname).first():
            flash(f'{reg_uname} is already taken.\n')
            
        reg_fname = request.form['fname']
        reg_lname = request.form['lname']
        reg_passw = request.form['pass']

        
    return render_template('signup.html', title='Sign Up')

if __name__ == "__main__":
    db.create_all()
    app.run(use_reloader=True, debug=True)