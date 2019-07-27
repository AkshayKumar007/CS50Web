# PYTHON version : 3.6.8 64-bit
import os
import requests

from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

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


@app.route("/")
def index():
        return render_template("index.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":#may need to change condition for post instead
        return render_template("register.html")
    else:
        fname = request.form.get("fname")
        passwd = request.form.get("passwd")
        uname = request.form.get("uname")
        email = request.form.get("email")
        if db.execute("SELECT * FROM users WHERE uname = :uname", {"uname": uname}).rowcount == 0:
            # return render_template("error.html", message="No such flight with that id.")
            db.execute("INSERT INTO users (fname, passwd, uname, email) VALUES (:fname, :passwd, :uname, :email)",
                {"fname":fname, "passwd":passwd, "uname":uname, "email":email})
            db.commit()
            return render_template("search.html")
        else:
            return render_template("error.html", message = " User already exists! ")


@app.route("/search", methods=["POST"])
def search():
    session["username"] = request.form.get("name")
    uname = request.form.get("name")
    passwd = request.form.get("passwd")
    if (db.execute("SELECT * FROM users WHERE uname = :uname AND passwd = :passwd", {"uname":uname, "passwd":passwd})).rowcount == 1 :
        res = (db.execute("SELECT * FROM users WHERE uname = :uname AND passwd = :passwd", {"uname":uname, "passwd":passwd})).fetchone()
        search.u_id = res.id # function attribute
        session["user_id"] = res.id
        return render_template("search.html")
    else:
        return render_template("error.html", message = "Invalid User Name or Password!")


@app.route("/results", methods=["POST"])# update all for partial searches
def results():
    srch_ele = request.form.get("search_element")
    if db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn":f"%{srch_ele}%"}).rowcount == 0:
        if db.execute("SELECT * FROM books WHERE author LIKE :author", {"author":f"%{srch_ele}%"}).rowcount == 0:        
            if db.execute("SELECT * FROM books WHERE title LIKE :title", {"title":f"%{srch_ele}%"}).rowcount == 0:
               return render_template("error.html", message=" Sorry! No such book found. ") 
            else:
                res1 = db.execute("SELECT * FROM books WHERE title LIKE :title", {"title":f"%{srch_ele}%"}).fetchall()
                return render_template("results.html", res1 = res1, res2 = None)
        else:
            res1 = db.execute("SELECT * FROM books WHERE author LIKE :author", {"author":f"%{srch_ele}%"}).fetchall()
            res2 = db.execute("SELECT * FROM books WHERE title LIKE :title", {"title":f"%{srch_ele}%"}).fetchall()
            return render_template("results.html", res1 = res1, res2 = res2)
    else:
        res1 = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn":f"%{srch_ele}%"}).fetchall()
        return render_template("results.html", res1 = res1, res2 = None)


@app.route("/review/<int:book_id>", methods=["GET", "POST"])
def review(book_id):
    stars = [1,2,3,4,5]
    if request.method == "GET":
        res = db.execute("SELECT * FROM books WHERE id = :book_id",{"book_id":book_id}).fetchone()
        if res is None:
            return render_template("error.html", message = "Sorry! No information found")
        else :
            rev_stat = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"2mMchqfNt2KiRN8KOZB3g", "isbns":res.isbn})            
            r1 = rev_stat.json()
            avg_rev = r1["books"][0]["average_rating"]
            rev_cnt = r1["books"][0]["work_ratings_count"]
            my_res = db.execute("SELECT * FROM reviews WHERE b_id = :b_id ORDER BY id DESC LIMIT 10",{"b_id":book_id}).fetchall()
            #if my_res is none, create template for that case as well
            return render_template("review.html", id = res.id, btitle = res.title, author = res.author, year = res.year, isbn = res.isbn, count = rev_cnt, avg = avg_rev, result = my_res , stars = stars)
    # more stuff to do
    elif request.method == "POST":
        rate = request.form.get("rate")
        revw = request.form.get("revw")
        # ensure user puts only one review
        checker = db.execute("SELECT * FROM reviews WHERE u_id = :u_id AND b_id = :b_id",{"u_id":session["user_id"], "b_id":book_id}).fetchone()
        if checker is None:
            db.execute("INSERT INTO reviews (u_id, b_id, rating, review, user_name) VALUES(:u_id, :b_id, :rate, :revw, :user_name)",\
                {"u_id":session["user_id"], "b_id":book_id,"rate":rate, "revw":revw, "user_name":session["username"]})# if session userid doesn't work use search.u_id attribute in search route || session["user_id"]
            db.commit()
            res = db.execute("SELECT * FROM books WHERE id = :book_id",{"book_id":book_id}).fetchone()
            rev_stat = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"2mMchqfNt2KiRN8KOZB3g", "isbns":res.isbn})
            r1 = rev_stat.json()
            avg_rev = r1["books"][0]["average_rating"]
            rev_cnt = r1["books"][0]["work_ratings_count"]
            my_res = db.execute("SELECT * FROM reviews WHERE b_id = :b_id ORDER BY id DESC LIMIT 10",{"b_id":book_id}).fetchall()
            return render_template("review.html", id = res.id,  btitle = res.title, author = res.author, year = res.year, isbn = res.isbn, count = rev_cnt, avg = avg_rev, result = my_res, stars = stars)
        else:
            db.execute("UPDATE reviews SET rating = :rate WHERE u_id = :u_id AND b_id = :b_id",{"u_id":session["user_id"], "b_id":book_id, "rate":rate})
            db.execute("UPDATE reviews SET review = :revw  WHERE u_id = :u_id AND b_id = :b_id",{"u_id":session["user_id"], "b_id":book_id, "revw":revw})   
            db.commit()
            res = db.execute("SELECT * FROM books WHERE id = :book_id",{"book_id":book_id}).fetchone()
            rev_stat = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"2mMchqfNt2KiRN8KOZB3g", "isbns":res.isbn})
            r1 = rev_stat.json()
            avg_rev = r1["books"][0]["average_rating"]
            rev_cnt = r1["books"][0]["work_ratings_count"]
            my_res = db.execute("SELECT * FROM reviews WHERE b_id = :b_id ORDER BY id DESC LIMIT 10",{"b_id":book_id}).fetchall()
            return render_template("review.html", id = res.id, btitle = res.title, author = res.author, year = res.year, isbn = res.isbn, count = rev_cnt, avg = avg_rev, result = my_res, stars = stars)


@app.route("/api/<string:isbn>")
def flight_api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid ISBN"}), 404
    rev_stat = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"2mMchqfNt2KiRN8KOZB3g", "isbns":isbn})            
    r1 = rev_stat.json()
    avg_rev = r1["books"][0]["average_rating"]
    rev_cnt = r1["books"][0]["work_ratings_count"]
    return jsonify({"title": book.title, "author": book.author, "year": book.year, "isbn": isbn, "review_count": avg_rev, "average_score": rev_cnt})

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))