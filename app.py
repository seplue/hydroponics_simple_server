from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import measurement_handling
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disables SQLAlchemy's event system
db = SQLAlchemy(app)
logging.basicConfig(level=logging.DEBUG)
a = app.logger


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
    return "fine"


@app.route('/measurement', methods=['POST'])
def measurement():
    a.debug('accessing route /measurement')
    content = request.json
    a.debug(type(content))
    a.debug(content)
    my_measurement = Measurement(temperature=content['temperature'],
                                 humidity=content['humidity'],
                                 light_intensity=content['light_intensity'])

    a.debug(repr(my_measurement))
    db.session.add(my_measurement)
    db.session.commit()
    a.debug(repr(my_measurement))
    return jsonify(content)


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


@app.route('/db_exp')
def db_exp():
    my_measurement = Measurement(temperature=1, humidity=2, pressure=3)
    db.session.add(my_measurement)
    db.session.commit()
    return repr(my_measurement)


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temperature = db.Column(db.DECIMAL)
    humidity = db.Column(db.DECIMAL)
    light_intensity = db.Column(db.DECIMAL)

    def __repr__(self):
        return f"{self.id}, {self.date_posted}, {self.temperature},{self.humidity}, {self.light_intensity}"


if __name__ == '__main__':
    app.run()
