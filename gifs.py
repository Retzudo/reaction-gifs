from flask import Flask, render_template, abort, jsonify, send_file
from flask_cors import CORS
import yaml

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gifs.json')
def gifs():
    try:
        with open('./gifs.yaml') as f:
            data = yaml.load(f.read())
    except (IOError, yaml.scanner.ScannerError):
        abort(404)

    return jsonify(data)


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')
