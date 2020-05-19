from flask import Flask, session, render_template, request, url_for, redirect
from flask_session import Session
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


data = None

@app.route("/", methods=["POST", "GET"])
def index():
    title = "Home"
    if(data == None):
        return render_template("index.html", title=title, login=False)
    return render_template("index.html", title=title, login=True)


@app.route("/login", methods=["POST"])
def login():
    username_fill = request.form.get("loginEmail")
    password_fill = request.form.get("loginPass")
    user = User.query.filter_by(username=username_fill).first()

    if(not(user is None)):
        if(user.password==password_fill):
            global data 
            data = {
                'Email': user.username,
                'First Name' : user.first_name,
                'Last Name' : user.last_name
            }
    return redirect(url_for('.index'))

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("registerEmail")
    password = request.form.get("registerPass")
    password2 = request.form.get("registerPass2")
    if(password==password2):
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('.index'))

@app.route("/logout")
def logout():
    global data
    data = None
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