from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import measurement_handling
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disables SQLAlchemy's event system
db = SQLAlchemy(app)
logging.basicConfig(level=logging.INFO)
a = app.logger


@app.route('/')
def hello_world():  # put application's code here
    a.info('info')
    return 'Hello World!'


@app.route('/test_put', methods=['PUT', 'POST'])
def test_put():
    a.info('accessing route /test_put')
    a.debug(request)
    content = request.json
    a.debug(content)
    a.debug(type(content))
    return "fine"


@app.route('/measurement', methods=['POST'])
def measurement():
    a.info('accessing route /measurement')
    content = request.json
    a.debug(f"type of content: {type(content)}")
    a.debug(f"content: {content}")
    # we have to check if the time_utc has been set
    a.debug(f"type of time_utc: {type(content['time_utc'])}")
    """my_measurement = Measurement(temperature=content['temperature'],
                                 humidity=content['humidity'],
                                 light_intensity=content['light_intensity'])"""
    my_measurement = Measurement()
    for key, value in content.items():
        try:
            setattr(my_measurement, key, value)
        except Exception as e:
            a.warning(e)

    a.debug(f"before adding to db.session: {repr(my_measurement)}")
    try:
        db.session.add(my_measurement)
        db.session.commit()
    except Exception as e:
        a.warning(e)
    a.info(f"The following entry was added to db:\n {repr(my_measurement)}")
    return jsonify(content)


@app.route('/last_measurement')
def last_measurement():
    a.info('accessing route /last_measurement')
    my_last_measurement = Measurement.query.order_by(Measurement.id.desc()).first()
    a.debug(f"{str(my_last_measurement)}")
    return str(my_last_measurement)


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temperature = db.Column(db.DECIMAL)
    humidity = db.Column(db.DECIMAL)
    light_intensity = db.Column(db.DECIMAL)
    pressure = db.Column(db.DECIMAL)

    def __repr__(self):
        return f"{self.id}, " \
               f"{self.date_posted}, " \
               f"{self.temperature}, " \
               f"{self.humidity}, " \
               f"{self.light_intensity}, " \
               f"{self.pressure}"

    def __str__(self):
        return f"ID: {self.id}, \n" \
               f"Date: {self.date_posted}, \n" \
               f"Temperature: {self.temperature}, \n" \
               f"Humidity: {self.humidity}, \n" \
               f"Light intensity: {self.light_intensity}, \n" \
               f"Pressure: {self.pressure}"


if __name__ == '__main__':
    app.run()
