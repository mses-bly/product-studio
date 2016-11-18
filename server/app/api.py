import sqlite3

import flask
from flask import Flask
from flask import g
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

DATABASE = 'image_db.db'


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def isJsonContent(request):
    return 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'


@app.route('/get_image', methods=['GET'])
def get_image():
    return _get_image(), 200


@app.route('/push_image', methods=['POST'])
def push_image():
    if request.method == 'POST' and isJsonContent(request):
        put_image(request.json['data'])
    return flask.jsonify({"response": "ALL GOOD"}), 200


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def modify_db(query, args=()):
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()


def put_image(image):
    # clear db first
    modify_db("""delete from images""")

    # then add our only image
    modify_db("""insert into images values ('%s')""" % image)


def _get_image():
    return query_db('select image from images limit 1')[0][0]


if __name__ == "__main__":
    app.run(debug=True, processes=5)
