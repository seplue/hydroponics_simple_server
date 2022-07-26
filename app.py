from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import measurement_handling
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
logging.basicConfig(level=logging.DEBUG)
a = app.logger


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temperature = db.Column(db.DECIMAL)
    humidity = db.Column(db.DECIMAL)
    pressure = db.Column(db.DECIMAL)

    def __repr__(self):
        return f"{self.id}, {self.date_posted}, {self.temperature},{self.humidity}, {self.pressure}"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


@app.route('/')
def hello_world():  # put application's code here
    a.info('info')
    return 'Hello World!'


@app.route('/test_put', methods=['PUT', 'POST'])
def test_put():
    a.debug('function called: test_put')
    a.debug(request)
    content = request.json
    a.debug(content)
    a.debug(type(content))
    measurement_handling.add_measurement(content)
    return "fine"


@app.route('/measurement', methods=['PUT', 'POST'])
def measurement():
    a.debug('measurement')
    content = request.get_json(silent=True)
    a.debug(type(content))
    a.debug(content)
    return content


@app.route('/query-example')
def query_example():
    return 'Query String Example'


@app.route('/form-example')
def form_example():
    return 'Form Data Example'


@app.route('/json-example')
def json_example():
    return 'JSON Object Example'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('user', usr=user))
    else:
        return render_template('login.html')


@app.route('/<usr>')
def user(usr):
    return f'<h1>{usr}</h1>'


if __name__ == '__main__':
    app.run()
