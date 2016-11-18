import flask
from flask import Flask
from flask import request

app = Flask(__name__)

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401


def isJsonContent(request):
    return 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'


@app.route('/push_image', methods=['POST'])
def push_image():
    if request.method == 'POST' and isJsonContent(request):
        print request.json['data']
    return flask.jsonify({"response": "ALL GOOD"}), HTTP_OK


if __name__ == "__main__":
    app.run(debug=True, processes=5)
