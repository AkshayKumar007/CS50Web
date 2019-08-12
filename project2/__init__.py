import os, requests, datetime, threading

from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

#add if condition to check for pre-existing channels
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
            dname = [ row[0][1] for row in res ]
            session['username'] = dname
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
                # return render_template("channel_list.html")
            else:
                return jsonify({"message" : "no_dname"})
                #add js code for displayname taken
        else:
            return jsonify({"message" : "no_mail"})
            # add js code for user already exists

@app.route("/channel_list", methods = ["GET", "POST"])
def channel_list():
    # if request.method == "POST":
    #     email = request.form.get("email")
    #     passwd = request.form.get("passwd")
    #     if db.execute("SELECT * FROM users1 WHERE email = :email AND passwd = :passwd ",{"email":email, "passwd":passwd}).rowcount == 1:
    #         dname = db.execute("SELECT dname FROM users1 WHERE email = :email AND passwd = :passwd ",{"email":email, "passwd":passwd})
    #         session['username'] = dname
    #         return jsonify({"message" : "success"})
    #         # return render_template("channel_list.html", Channel = list(channels.keys()))
    #     else:
    #         # goes to index.html
    #         return jsonify({"message" : "wrong"}) #need to add js file for this.
    if request.method == "GET":
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
                channels[cname] = []
            return jsonify({"message" : "success"})
        # , "dname" : session['username'], "Channel" : list(channels.keys())
            # return render_template("channel_list.html", dname = session['username'], Channel = list(channels.keys()))


@app.route("/channel/<string:chnl>", methods=["GET", "POST"])
def channel(chnl):
    if request.method == "GET":
        if chnl in channels:
            return render_template("channel.html", dname = session['username'], Channel = channels[chnl])
        
    elif request.method == "POST":
        message = request.form.get("message")
        uname = session["username"]
        time = datetime.now()
        #update channel content using sockets
        channels[chnl].append((message, uname, time))
        

@socketio.on("send message")
def vote(data):
    # selection = data["selection"]
    message = data["selection"]
    uname = session["username"]
    time = datetime.now()
    selection = {"message":message, "uname": uname, "time":time}
    emit("announce message", {"selection": selection}, broadcast=True)


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

if __name__ == "__main__":
    socketio.run(app)#may heal our pickle problem

# channel(dict) => channel_names(string) => (message+dname+timestamp)(list of tuples)            

#  channel _list alpha

# if request.method == "POST":#from index
#         temp = request.form.get("dname")
#         if session.get(temp, None) == None:
#             session["username"] = request.form.get("dname")
#         return render_template("chnl_list.html", channel = channel.keys())
    
    
#if request.method == "GET":#from register
#   cname = request.form.get("cname")
#       if cname in channel:
#           pass
