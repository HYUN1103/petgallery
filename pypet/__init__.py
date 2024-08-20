from flask import Flask,render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_socketio import SocketIO,emit
from engineio.async_drivers import gevent
import config, logging


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
socketio = SocketIO()



def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    
    from . import models
    
    # 블루프린트
    from .views import main_views, question_views, answer_views, \
        auth_views, card_views, upload_views, upchat_views, hosp_views, gallery, home, upload, hosp, upchat
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(upload_views.bp)
    app.register_blueprint(upchat_views.bp)
    app.register_blueprint(card_views.bp)
    app.register_blueprint(hosp_views.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(gallery.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(hosp.bp)
    app.register_blueprint(upchat.bp)
    
    
    
    # SocketIO 초기화
    socketio.init_app(app, cors_allowed_origins='*', async_mode='eventlet')
    socketio.run(app, port=5000, debug=True)
    return app

# 클라이언트가 보낸 건 서버가 받는 부분
# message, namespace='/chating' 필요하면 붙
@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))
    #broadcast=전부한테 보낸다 
    socketio.emit('message', data)

if __name__ == "__main__":
    app = create_app()
    # logging.info("앱이 시작되었습니다.")
    #socketio가 설정이 된 상태에서 @socketio.on을 사용할 수 있다
    socketio.run(app, debug=True)
    
