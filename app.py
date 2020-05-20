from flask import Flask, session, render_template, request, url_for, redirect
from flask_session import Session
from authlib.integrations.flask_client import OAuth
from models import *
from hashPassword import *
import time

app = Flask(__name__)

# Configure session to use filesystem
app.config["PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

data = None

@app.route("/")
def index():
    title = "Home"
    if(data == None):
        return render_template("index.html", title=title, login=False)
    return render_template("index.html", title=title, login=True, name=data['First Name'][0].capitalize()+data['First Name'][1:])

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
    global data
    data = {
        'Email' : user_info['email'],
        'First Name' : user_info['given_name'],
        'Last Name' : user_info['family_name']
    }    
    user = User.query.filter_by(username=data['Email']).first()
    
    # if user is new, add to database with default PASSWORD = admin1234
    if(user is None):
        new_user = User(username=data['Email'], password=hash_password('admin1234'), first_name=data['First Name'], last_name=data['Last Name'])
        db.session.add(new_user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
    else:
        data = {
            'Email': user.username,
            'First Name': user.first_name,
            'Last Name': user.last_name
        } 

    time.sleep(1)  
    return redirect(url_for('.index'))

@app.route("/login", methods=["POST", "GET"])
def login():
    title = "Login"
    if(request.method=="POST"):
        username_fill = request.form.get("loginEmail")
        password_fill = request.form.get("loginPass")
        user = User.query.filter_by(username=username_fill).first()

        if(not(user is None)):
            if(verify_password(user.password, password_fill)):
                global data 
                data = {
                    'Email': user.username,
                    'First Name' : user.first_name,
                    'Last Name' : user.last_name
                }
                time.sleep(1)
                return redirect(url_for('.index'))
        return redirect(url_for('.login', wrong=True))
    else:
        if(data!=None):
            return redirect(url_for('.index'))
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
        time.sleep(1)
        return redirect(url_for('.index'))
    else:
        if(data!=None):
            return redirect(url_for('.index'))
        return render_template("register.html", title=title)

@app.route("/l1o1g1o1u1t")
def logout():
    global data
    data = None
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