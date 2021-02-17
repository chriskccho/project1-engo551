import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://xhwxmfktruxsfd:130d2b3ee2fd541fc239ce7ab21c07acd0a4c3c1418e4a349ab0d7bf0fc3fd6e@ec2-54-162-119-125.compute-1.amazonaws.com:5432/dbi2qh6irek481"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
