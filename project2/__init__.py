import os, requests, threading, json

from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime as dt

from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

channels = {"#general":[]} # to store channels and respective messages
# 'C'hannel for passing to DOMs

@app.route("/")
def index():
    # if 'username' in session:
    #     return redirect(url_for('channel_list'))
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        passwd = request.form.get("passwd")
        if db.execute("SELECT * FROM users1 WHERE email = :email AND passwd = :passwd ",{"email":email, "passwd":passwd}).rowcount == 1:
            res = db.execute("SELECT dname FROM users1 WHERE email = :email AND passwd = :passwd ",{"email":email, "passwd":passwd})
            dname = [ row[0] for row in res ]
            session['username'] = dname[0]
            return jsonify({"message" : "success"})            
        else:
            return jsonify({"message" : "wrong"}) # goes to index.html


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    else:
    # if request.method == "POST":
        fname = request.form.get("fname")
        dname = request.form.get("dname")
        passwd = request.form.get("passwd")
        email = request.form.get("email")
        if db.execute("SELECT * FROM users1 WHERE email = :email",{"email":email}).rowcount == 0:
            if db.execute("SELECT * FROM users1 WHERE dname = :dname",{"dname":dname}).rowcount == 0:
                db.execute("INSERT INTO users1 (fname, dname, passwd, email) VALUES (:fname, :dname, :passwd, :email)"\
                    ,{"fname":fname, "dname":dname, "passwd":passwd, "email":email})
                db.commit()
                session['username'] = dname
                return jsonify({"message" : "success"})
                
            else:
                return jsonify({"message" : "no_dname"})
         
        else:
            return jsonify({"message" : "no_mail"})
           

@app.route("/channel_list")
def channel_list():
    # if request.method == "GET":
    return render_template("channel_list.html", dname = session['username'], Channel = list(channels.keys()))

    
@app.route("/create_channel", methods=["POST"])
def create_channel():
    if request.method == "POST":
        cname = request.form.get("cname")
        if cname in channels:
            return jsonify({"message" : "exists"})
        else:
            # write statements as per our dictionary structure to add new channel
            if channels.get(cname, None) == None:#maybe redunadnt
                if cname[0] != '#':
                    cname = '#' + cname[:]
                channels[cname] = []
            return jsonify({"message" : "success"})
        # , "dname" : session['username'], "Channel" : list(channels.keys())
            # return render_template("channel_list.html", dname = session['username'], Channel = list(channels.keys()))


@app.route("/channel/<string:chnl>", methods=["GET", "POST"])
def channel(chnl):
    vote.chnl = chnl #newly added after chrome-revelations
    if request.method == "GET":
        if chnl in channels:
            return render_template("channel.html", dname = session['username'], Channel = channels[chnl], channel_name = chnl)
     
        
@socketio.on('send messages')
def vote(data):
    messages = data['messages']
    time = data['time']
    dname = session["username"]
    channels[vote.chnl].append((messages, dname, time))
    emit('announce messages', {"messages": messages, "dname": dname, "time": time}, broadcast=True)
    

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return render_template("logout.html")


if __name__ == "__main__":
    socketio.run(app)
