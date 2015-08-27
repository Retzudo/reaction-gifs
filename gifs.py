from flask import Flask, render_template, Response, abort

app = Flask(__name__)


@app.route('/', )
def index():
    return render_template('index.html')


@app.route('/gifs')
def gifs():
    try:
        with open('./gifs.json') as f:
            data = f.read()
    except IOError:
        abort(404)

    return Response(data, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
