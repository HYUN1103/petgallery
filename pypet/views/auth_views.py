import functools

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from sqlalchemy.exc import IntegrityError

from pypet import db
from pypet.forms import UserCreateForm, UserLoginForm, DeleteAccountForm  
from pypet.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            try:
                user = User(username=form.username.data,
                            password=generate_password_hash(
                                form.password1.data),
                            email=form.email.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.home'))
            except IntegrityError:
                db.session.rollback()
                flash('이미 존재하는 사용자 이름 또는 이메일입니다.')
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    # 사용자 로그인 폼 객체 생성
    form = UserLoginForm()
    # 요청이 POST 방식이고 폼이 유효한 경우
    if request.method == 'POST' and form.validate_on_submit():
        error = None  # 오류 메시지 변수 초기화
        # 사용자명을 기준으로 사용자 조회
        user = User.query.filter_by(username=form.username.data).first()
        # 사용자가 존재하지 않는 경우
        if not user:
            error = "존재하지 않는 사용자입니다."
        # 비밀번호가 올바르지 않은 경우
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        # 오류가 없는 경우 (로그인 성공)
        if error is None:
            session.clear()  # 세션 초기화
            session['user_id'] = user.id  # 사용자 ID를 세션에 저장

            _next = request.args.get('next', '')  # 리다이렉트할 URL 가져오기
            if _next:
                return redirect(_next)  # 지정된 URL로 리다이렉트
            else:
                return redirect(url_for('main.home'))  # 기본 홈 페이지로 리다이렉트

        flash(error)  # 오류 메시지를 플래시로 표시
    # GET 요청이거나 폼이 유효하지 않은 경우 로그인 템플릿 렌더링
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        # 사용자가 로그인되지 않은 경우
        if g.user is None:
            # 현재 요청이 GET 요청인 경우, 다음 URL을 현재 URL로 설정
            _next = request.url if request.method == 'GET' else ''
            # 로그인 페이지로 리다이렉트, 'next' 매개변수에 리다이렉트 후 돌아올 URL 포함
            return redirect(url_for('auth.login', next=_next))
        # 사용자가 로그인된 경우, 원래 뷰 함수를 호출하여 계속 진행
        return view(*args, **kwargs)
    # wrapped_view 함수 반환
    return wrapped_view


# 프로필
@bp.route('/profile')
@login_required
def profile():
    form = UserLoginForm()
    return render_template('auth/profile.html', form=form)

#삭제
@bp.route('/auth/delete_account', methods=['POST', 'GET'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if check_password_hash(g.user.password, form.password.data):
            db.session.delete(g.user)
            db.session.commit()
            flash('계정이 성공적으로 삭제되었습니다.')
            return redirect(url_for('auth.login'))
        else:
            flash('비밀번호가 올바르지 않습니다.')
    return render_template('auth/delete_account.html', form=form)





