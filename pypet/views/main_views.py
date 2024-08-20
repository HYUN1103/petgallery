from flask import Blueprint, render_template, redirect, url_for, session, g,jsonify
from pypet.models import Question, User
from pypet.models import Question, Card

bp = Blueprint('main', __name__, url_prefix='/')


# # 홈화면
@bp.route('/')
def home():
    return render_template('home/home.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

#게시판화면
@bp.route('/list')
def index():
    return redirect(url_for('question._list'))

#갤러리카드
@bp.route('/cards')
def get_cards():
    if g.user is None:
        return jsonify([]), 401
    
    cards = Card.query.filter_by(user_id=g.user.id).all()
    card_list = [{
        'id': card.id,
        'title': card.title,
        'text': card.text,
        'image_url': card.image_url
    } for card in cards]
    
    return jsonify(card_list)

