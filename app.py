from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado:', request.sid)
    emit('load_messages', messages)

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado:', request.sid)

@socketio.on('new_message')
def handle_new_message(data):
    message = {
        'id': len(messages) + 1,
        'text': data['text'],
        'username': data['username']
    }
    messages.append(message)
    emit('broadcast_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)