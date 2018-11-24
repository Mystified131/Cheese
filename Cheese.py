from flask import Flask, request, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime, os, cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Cheese:Jackson1313@localhost:8889/Cheese'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

class Cheese(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(120))
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))

    def __init__(self, timestamp, name, description):
        self.timestamp = timestamp
        self.name = name
        self.description = description

@app.route("/", methods =['GET'])
def main():
     right_now = datetime.datetime.now().isoformat()
     list = []

     for i in right_now:
        if i.isnumeric():
           list.append(i)

     tim = "".join(list)
     session['timestamp'] = tim
     return redirect ('/index')

@app.route("/index", methods =['GET', 'POST'])
def index():
    cheeses = Cheese.query.all()
    return render_template('index.html', cheeses = cheeses, time = session['timestamp'])


@app.route("/add", methods =['GET', 'POST'])
def add():
    cheesename = request.form["name"]
    cheesedescript = request.form["descript"]
    timestamp = session['timestamp']
    name = cgi.escape(cheesename)
    description = cgi.escape(cheesedescript)
    new_cheese = Cheese(timestamp, name, description)
    db.session.add(new_cheese)
    db.session.commit()
    cheeses = Cheese.query.all()
    return render_template('index.html', cheeses = cheeses, time = session['timestamp'])

@app.route("/remove", methods =['GET', 'POST'])
def remove():
    cheesename = request.form["remname"]
    name = cgi.escape(cheesename)
    the_cheese = Cheese.query.filter_by(name=name).first()
    if the_cheese:
        db.session.delete(the_cheese)
        db.session.commit()
    cheeses = Cheese.query.all()
    return render_template('index.html', cheeses = cheeses, time = session['timestamp'])

if __name__ == '__main__':
    app.run()



