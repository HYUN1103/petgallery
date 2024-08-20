from flask import Blueprint, render_template
from flask_socketio import emit, send
import sqlite3
import logging
from pypet import socketio


bp = Blueprint('upchat', __name__, url_prefix='/upchat')

def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                (username TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@bp.route('/upchat')
def sock():
    return render_template('chating/chat.html')
    """_summary_
    클라이언트(html,js) - 메시지를 입력했음 → 메세지전송 →
    서버(py)쪽에서는 받는 애가 있음 → 서버가 클라이언트쪽으로 메세지를 전송
    클라이언트에서 서버가 전달하는 애를 받아야함
    """
logging.basicConfig(level=logging.INFO)

@socketio.on('message', namespace='/upchat')
def handle_message(msg):
    logging.info(f"Received message: {msg}")
    try:
        # 메시지를 데이터베이스에 저장
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (msg['username'], msg['message']))
        conn.commit()
        conn.close()
        logging.info("Message saved to database")
    except Exception as e:
        logging.error(f"Error saving message to database: {e}")
    
    try:
        # 모든 클라이언트에 메시지 전송
        send(msg, broadcast=True, namespace='/upchat')
        logging.info(f"Sent message to all clients: {msg}")
    except Exception as e:
        logging.error(f"Error sending message to clients: {e}")
