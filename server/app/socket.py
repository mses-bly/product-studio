from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('', namespace='/test')
def test_message(message):
    print "Image Received"
    emit('broadcast_image', message, broadcast=True)



@socketio.on('receive_image', namespace='/test')
def test_message(message):
    print "Image Received"
    emit('broadcast_image', message, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    print "Client connected!"

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
