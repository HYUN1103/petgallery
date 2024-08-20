from flask import Blueprint, render_template
from flask_socketio import emit
from pypet import socketio

bp = Blueprint('chating', __name__, url_prefix='/chating')

@bp.route('/chat')
def chat():
    return render_template('chating/chat.html')

@socketio.on('message', namespace='/chating')
def handle_message(data):
    print('received message: ' + str(data))
    emit('message', data, broadcast=True, namespace='/chating')
