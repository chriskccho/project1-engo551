import os
import sys
import requests
import json

from flask import Flask, session, request, jsonify, redirect, url_for, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.sql.expression import cast
import sqlalchemy

from flask import render_template
from flask_table import Table, Col

app = Flask(__name__)
app.secret_key = "1234"


from data import *
from models import *


app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://xhwxmfktruxsfd:130d2b3ee2fd541fc239ce7ab21c07acd0a4c3c1418e4a349ab0d7bf0fc3fd6e@ec2-54-162-119-125.compute-1.amazonaws.com:5432/dbi2qh6irek481"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/", methods = ["GET", "POST"])
def index():
    if not session.get('logged_in'):
        return render_template("homepage.html")
    else:
        comments = Comment.query.filter().all()
        return render_template("signedin.html", name=session.get('username'), comments=comments)

@app.route("/home", methods = ["GET","POST"])
def home():
    #name = request.form.get("name")
    if not session.get('logged_in'):
        return render_template("homepage.html")
    comments = Comment.query.filter().all()
    return render_template("signedin.html", name=session.get('username'), comments = comments)

@app.route("/signup", methods = ["GET","POST"])
def signup():
    return render_template("signup.html")

@app.route("/signedin", methods = ["POST"])
def signedin():

    if request.method == 'POST':
        session['username'] = request.form.get("name")
        session['password'] = request.form.get("password")
        check_username = accounts.query.filter(accounts.username.like(session.get('username'))).first()
    else:
        return render_template("homepage.html")

    if (check_username == None) or (check_username.username == session.get('username') and check_username.password != session.get('password')):
        session.pop('username', None)
        return render_template("incorrect_login.html", check_user=check_username)
    else:
        session['logged_in'] = True
        comments = Comment.query.filter().all()
        return render_template("signedin.html", name=session.get('username'), comments=comments)


@app.route("/books", methods = ["GET", "POST"])
def bookpage():
    book = books.query.filter().all()
    table = Data(book)

    if not session.get('logged_in'):
        return render_template("signup.html")

    return render_template("books.html", table=table)

@app.route("/results", methods = ["GET", "POST"])
def results():
    qry=request.form.get("query")

    result = books.query.filter((books.isbn.contains(qry)) | (books.title.contains(qry)) | (books.author.contains(qry)) | (cast(books.published, sqlalchemy.String).contains(qry))).all()
    selected_book = result
    result=Data(result)

    return render_template("results.html",query=qry, result=result, selected_book=selected_book)

@app.route("/created_account", methods = ["POST"])
def created_account():
    user = request.form.get("username")
    password = request.form.get("password")

    check_user = accounts.query.filter(accounts.username.like(user)).first()

    if check_user == None:
        new_account = accounts(username=user, password=password)
        db.session.add(new_account)
        db.session.commit()
        return render_template("created_account.html", name=user)
    else:
        return render_template("incorrect_login.html", check_user=check_user)

@app.route("/loggedout", methods = ["GET", "POST"])
def loggedout():
    session.clear()
    return render_template("loggedout.html")

@app.route("/gen_comments", methods = ["POST"])
def gen_comments():

    if not session.get('logged_in'):
        return render_template("signup.html")
    else:
        comment = request.form.get("comment")
        new_comment = Comment(name=session.get('username'), body=comment, timestamp=datetime.datetime.now())
        db.session.add(new_comment)
        db.session.commit()


        new_comment = Comment.query.filter().all()
        table = commentdis(new_comment)

        return render_template("signedin.html", table=table, name=session.get('username'), comments=new_comment)
