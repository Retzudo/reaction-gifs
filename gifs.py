from flask import Flask, render_template, abort, jsonify, send_file
import yaml

app = Flask(__name__)


@app.route('/', )
def index():
    return render_template('index.html')


@app.route('/gifs')
def gifs():
    try:
        with open('./gifs.yml') as f:
            data = yaml.load(f.read())
    except (IOError, yaml.scanner.ScannerError):
        abort(404)

    return jsonify(data)


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')


if __name__ == '__main__':
    app.run(debug=True)
