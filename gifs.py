from flask import Flask, render_template, abort, jsonify, send_file
from flask.ext.redis import FlaskRedis
import yaml

app = Flask(__name__)
redis_store = FlaskRedis(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gifs.json')
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


@app.route('/preview/<url>')
def preview(url):
    """Get the key `url` from redis and serve that data with
    MIME type 'image/gif'."""


def cache_previews():
    """Store preview images for GIFs listed in gifs.yml in redis.

    1. download the image to a temporary location
    2. extract the first frame of the gif using extract_frames.py
    3. store that data in redis under the GIF's URL as the key
    """

# Run immediately on startup
cache_previews()

if __name__ == '__main__':
    app.run(debug=True)
