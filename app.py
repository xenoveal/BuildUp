from flask import Flask, session, render_template, request, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from models import *
from hashPassword import *
import time
from datetime import timedelta

app = Flask(__name__)

# Configure session
app.secret_key = "xenoveals123"
app.config['SESSION_COOKIE_NAME'] = 'login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://fgaelkvcnxhqos:7784fabbd6c0316eb419e127eeb3e50ac6e5808fcc827204fe982cffe88b2a3c@ec2-52-44-55-63.compute-1.amazonaws.com:5432/d7s2do0pifj2qc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Google login
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="630158134949-pd5grh25vtme67brml89a69n5a5qo382.apps.googleusercontent.com",
    client_secret="IAwl2pMU7OUQl3CZ_Vt25qxC",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route("/")
def index():
    title = "Home"
    try:
        data = session['data']
        return render_template("index.html", title=title, login=True, name=data['First Name'][0].capitalize()+data['First Name'][1:])
    except:
        return render_template("index.html", title=title, login=False)
    

@app.route("/google-login")
def login_google():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['data'] = {
        'Email' : user_info['email'],
        'First Name' : user_info['given_name'],
        'Last Name' : user_info['family_name']
    }   
    data = session['data']
    user = User.query.filter_by(username=data['Email']).first()  
    time.sleep(2) 
    # if user is new, add to database with default PASSWORD = admin1234
    if(user is None):
        new_user = User(username=data['Email'], password=hash_password('admin1234'), first_name=data['First Name'], last_name=data['Last Name'])
        db.session.add(new_user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
    else:
        session['data'] = {
            'Email': user.username,
            'First Name': user.first_name,
            'Last Name': user.last_name
        } 
    session.permanent = True  
    return redirect(url_for('.index'))

@app.route("/login", methods=["POST", "GET"])
def login():
    title = "Login"
    if(request.method=="POST"):
        username_fill = request.form.get("loginEmail")
        password_fill = request.form.get("loginPass")
        user = User.query.filter_by(username=username_fill).first()
        time.sleep(2)
        if(not(user is None)):
            if(verify_password(user.password, password_fill)): 
                session['data'] = {
                    'Email': user.username,
                    'First Name' : user.first_name,
                    'Last Name' : user.last_name
                }
                return redirect(url_for('.index'))
        return redirect(url_for('.login', wrong=True))
    else:
        try:
            data = session['data']
            return redirect(url_for('.index'))
        except:
            wrong = request.args.get('wrong')
            return render_template("login.html", title=title, wrong=wrong)

@app.route("/register", methods=["POST", "GET"])
def register():
    title="Register"
    if(request.method=="POST"):
        username = request.form.get("registerEmail")
        password = request.form.get("registerPass")
        password2 = request.form.get("registerPass2")
        if(password==password2):
            first_name = username.split('@')[0]
            new_user = User(username=username, password=hash_password(password), first_name=first_name)
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return redirect(url_for('.register', wrong=True))
        return redirect(url_for('.index'))
    else:
        try:
            data = session['data']
            return redirect(url_for('.index'))
        except:
            wrong = request.args.get('wrong')
            return render_template("register.html", title=title, wrong=wrong)

@app.route("/l1o1g1o1u1t")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    time.sleep(1)
    return redirect(url_for('.index'))

@app.route("/blog")
def blog():
    title = "Blog"
    return render_template("content.html", title=title)

@app.route("/betatester")
def more():
    title = "Betatester"
    return render_template("betatester.html", title=title)

@app.route("/user")
def user():
    title = "User"
    return render_template("user.html", title=title)