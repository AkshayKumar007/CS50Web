import os , requests

from flask import Flask, render_template, request, session, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"): #may have to change url
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


channel = dict()

@app.route("/")
def index():
    return  render_template("index.html")

@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        fname = request.form.get("fname")
        dname = request.form.get("dname")
        passwd = request.form.get("passwd")
        email = request.form.get("email")
        if db.execute("SELECT * FROM users WHERE email = :email",{"email":fname}).count == 0:
            if db.execute("SELECT * FROM users WHERE dname = :dname",{"dname":dname}).count == 0:
                db.execute("INSERT INTO users (fname, dname, passwd, email) VALUES (:fname, :dname, :passwd, :email)"\
                    ,{"fname":fname, "dname":dname, "passwd":passwd, "email":email})
                return render_template("channel_list", dname = dname)
            else:
                pass #add js code for username taken
        else:
            pass # add js code for user already exists

@app.route("/channel_list", method = ["GET","POST"])
def channel_list():
    if request.method == "GET":
        temp = request.form.get("dname")
        if session.get(temp, None) == None:
            session["username"] = request.form.get("dname")
        return render_template("chnl_list.html")
    if request.method == "POST":

