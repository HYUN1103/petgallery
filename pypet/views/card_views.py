from flask import Blueprint, request, jsonify, g, current_app
from pypet import db
from pypet.models import Card
from werkzeug.utils import secure_filename
import os

bp = Blueprint('card', __name__, url_prefix='/card')

@bp.route('/add', methods=['POST'])
def add_card():
    data = request.form
    title = data['title']
    text = data['text']
    image = request.files['image']
    username = data['username']

    if g.user is None:
        return jsonify({'error': 'Unauthorized'}), 401

    image_filename = secure_filename(image.filename)
    image_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
    image.save(image_path)
    print(username)
    print(type(username))

    card = Card(
        user_id=g.user.id,
        title=title,
        text=text,
        image_url=f'/static/uploads/{image_filename}',  # 수정된 부분
        username=username
    )
    db.session.add(card)
    db.session.commit()

    return jsonify({'success': True, 'image_url': card.image_url})

@bp.route('/list', methods=['GET'])
def list_cards():
    # if g.user is None:
    #     return jsonify({'error': 'Unauthorized'}), 401
    # cards = Card.query.filter_by(user_id=g.user.id).all()
    
    cards = Card.query.all()  # 모든 카드 불러오기
    if g.user:
        username = g.user.username
    else:
        username = None
    card_list = [{
        'id': card.id,
        'title': card.title,
        'text': card.text,
        'image_url': card.image_url,
        'username': card.username,
        'login_user': username
    } for card in cards]
    
    return jsonify(card_list)

@bp.route('/delete/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = Card.query.get(card_id)
    
    if card is None or card.user_id != g.user.id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db.session.delete(card)
    db.session.commit()
    
    return jsonify({'success': True})

@bp.route('/update/<int:card_id>', methods=['POST'])
def update_card(card_id):
    card = Card.query.get(card_id)
    
    if card is None or card.user_id != g.user.id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.form
    card.title = data['title']
    card.text = data['text']
    
    if 'image' in request.files:
        image = request.files['image']
        image_filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
        image.save(image_path)
        card.image_url = os.path.join('/static/uploads', image_filename)
    
    db.session.commit()
    
    return jsonify({'success': True, 'image_url': card.image_url})
