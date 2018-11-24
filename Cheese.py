from flask import Flask, request, render_template, session
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

@app.route("/", methods =['GET', 'POST'])
def index():
    right_now = datetime.datetime.now().isoformat()
    list = []

    for i in right_now:
        if i.isnumeric():
           list.append(i)

    tim = "".join(list)
    session['timestamp'] = tim
    cheeses = Cheese.query.all()
    cheeselist = []
    for cheese in cheeses:
        cheesestr = cheese.name + ": " + cheese.description
        cheeselist.append(cheesestr)
    cheeselist.sort()
    return render_template('index.html', cheeses = cheeselist)


@app.route("/add", methods =['GET', 'POST'])
def add():
    error = ""
    cheesename = request.form["name"]
    cheesedescript = request.form["descript"]
    timestamp = session['timestamp']
    name = cgi.escape(cheesename)
    name = name.lower()
    description = cgi.escape(cheesedescript)
    old_cheese = Cheese.query.filter_by(name=name).first()
    if old_cheese or not name or not description:
        if not description:
            error = "Please describe the cheese, in order to add it."
        if not name:
            error = "There is no cheese with no name."
        if old_cheese:
            error = "That cheese is already in the database."
        cheeses = Cheese.query.all()
        cheeselist = []
        for cheese in cheeses:
            cheesestr = cheese.name + ": " + cheese.description
            cheeselist.append(cheesestr)
        cheeselist.sort()
        return render_template('index.html', cheeses = cheeselist, error = error)
    new_cheese = Cheese(timestamp, name, description)
    db.session.add(new_cheese)
    db.session.commit()
    cheeses = Cheese.query.all()
    cheeselist = []
    for cheese in cheeses:
        cheesestr = cheese.name + ": " + cheese.description
        cheeselist.append(cheesestr)
    cheeselist.sort()
    return render_template('index.html', cheeses = cheeselist)

@app.route("/remove", methods =['GET', 'POST'])
def remove():
    cheesename = request.form["remname"]
    name = cgi.escape(cheesename)
    the_cheese = Cheese.query.filter_by(name=name).first()
    if the_cheese:
        db.session.delete(the_cheese)
        db.session.commit()
        cheeses = Cheese.query.all()
        cheeselist = []
        for cheese in cheeses:
            cheesestr = cheese.name + ": " + cheese.description
            cheeselist.append(cheesestr)
        cheeselist.sort()
        return render_template('index.html', cheeses = cheeselist)
    else:
        error2 = "That cheese is not in the database."
        cheeses = Cheese.query.all()
        cheeselist = []
        for cheese in cheeses:
            cheesestr = cheese.name + ": " + cheese.description
            cheeselist.append(cheesestr)
        cheeselist.sort()
        return render_template('index.html', cheeses = cheeselist, error2 = error2)

if __name__ == '__main__':
    app.run()



