from pypet import db
from datetime import datetime


question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)
#Question :질문 모델
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
    view_count = db.Column(db.Integer, default=0)   # 조회수를 저장하는 필드
    

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)        
    
#답변모델
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #답변을 질문과 연결하기 위해 추가 [question.id는 question테이블의 id를 의미한다.] , [ondelete: 삭제연동 = 질문을 삭제하면 질문에 달린 답글도 삭제]
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


# 사용자 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  #관리자인지 여부를 확인하는 필더
# 갤러리 정의
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='cards')


User.cards = db.relationship('Card', order_by=Card.create_date, back_populates='user')

# 동영상 모델 정의
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 동영상의 고유 ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 연관된 사용자의 ID
    username = db.Column(db.String(150), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)  # 동영상의 제목
    content = db.Column(db.Text, nullable=False)  # 동영상의 설명
    video_url = db.Column(db.String(300), nullable=False)  # 동영상의 URL
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user = db.relationship('User', back_populates='videos')  # 사용자와의 관계 설정

User.videos = db.relationship('Video', order_by=Video.create_date, back_populates='user')  # 사용자와 동영상의 관계 설정




