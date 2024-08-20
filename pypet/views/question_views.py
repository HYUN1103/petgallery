from datetime import datetime
from flask import Blueprint, render_template, request, url_for, session, g, flash, jsonify
from werkzeug.utils import redirect

from .. import db
from ..models import Question, Answer, User
from ..forms import QuestionForm, AnswerForm
from pypet.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

#질문목록

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

#상세페이지
# @bp.route('/detail/<int:question_id>/')
# def detail(question_id):
#     question = Question.query.get_or_404(question_id)
#     return render_template('question/question_detail.html', question=question) 

# 질문 상세 페이지
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    print(f"Before increment: {question.view_count}")  # 디버그용 출력
    question.view_count += 1
    db.session.commit()
    print(f"After increment: {question.view_count}")  # 디버그용 출력
    return render_template('question/question_detail.html', question=question, form=form)


#질문등록
@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    #request.method는 create 함수로 요청된 전송 방식을 의미
    #form.validate_on_submit 함수는 전송된 폼 데이터의 정합성을 점검
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

#삭제권한여부 /#관리자 권한을 확인하는 로직
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))



@bp.route('/vote/<int:question_id>/', methods=['POST'])
@login_required
def vote(question_id):
    try:
        _question = Question.query.get_or_404(question_id)
        if g.user == _question.user:
            return jsonify({'message': '본인이 작성한 글은 추천할 수 없습니다'}), 400
        else:
            if g.user not in _question.voter:
                _question.voter.append(g.user)
                db.session.commit()
                return jsonify({'voter_count': len(_question.voter)})
            else:
                return jsonify({'message': '이미 추천한 글입니다'}), 400
    except Exception as e:
        print(f"Error: {e}")  # 디버깅 정보를 서버 로그에 출력
        return jsonify({'message': '추천 처리 중 에러가 발생했습니다', 'error': str(e)}), 500
