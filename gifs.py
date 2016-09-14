import os
import yaml
import logging
from flask import Flask, render_template, abort, jsonify, send_file, Response
from flask_redis import FlaskRedis
from extract_frames import extract_frames
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.error import HTTPError

app = Flask(__name__)
app.config['REDIS_URL'] = os.environ.get(
    'GIFS_REDIS_URL',
    'redis://localhost:6379/0'
)
redis_store = FlaskRedis(app)
logging.basicConfig(level=logging.INFO)


def load_gifs():
    with open('./gifs.yml') as f:
        return yaml.load(f.read())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gifs.json')
def gifs():
    try:
        data = load_gifs()
    except (IOError, yaml.scanner.ScannerError):
        abort(404)

    return jsonify(data)


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')


@app.route('/preview/<path:url>')
def preview(url):
    """Get the key `url` from redis and serve that data with
    MIME type 'image/gif'."""
    gif_data = redis_store.get('{}:preview'.format(url))
    if gif_data is None:
        abort(404)

    return Response(gif_data, mimetype='image/gif')


@app.route('/gif/<path:url>')
def gif(url):
    gif_data = redis_store.get('{}'.format(url))
    if gif_data is None:
        abort(404)

    return Response(gif_data, mimetype='image/gif')


def cache_previews():
    """Store preview images for GIFs listed in gifs.yml in redis.

    1. download the image to a temporary location
    2. extract the first frame of the gif using extract_frames.py
    3. store that data in redis under the GIF's URL as the key
    """
    for gif in load_gifs()['gifs']:
        # Download to a tempfile
        if redis_store.exists(gif['url']):
            # Skip downloading if that GIF is already in redis
            break
        with NamedTemporaryFile(prefix='tmp_gif_', suffix='.gif') as tmp_file:
            try:
                logging.info(
                    'Downloading GIF at "{}" to "{}"'.format(
                        gif['url'],
                        tmp_file.name
                    )
                )
                data = urlopen(gif['url']).read()
                tmp_file.write(data)

                # extract and set value in redis
                redis_store.set(
                    '{}:preview'.format(gif['url']),
                    next(extract_frames(tmp_file.name)).getvalue()
                )

                # store gif in redis
                redis_store.set(
                    gif['url'],
                    data
                )

            except HTTPError as e:
                logging.warning('Could not download image: {}'.format(e))


# Run immediately on startup
cache_previews()

if __name__ == '__main__':
    app.run(debug=True)
