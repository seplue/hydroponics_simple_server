from flask import Flask, redirect, url_for, render_template, request, jsonify
import measurement_handling
import logging
app = Flask(__name__)
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
