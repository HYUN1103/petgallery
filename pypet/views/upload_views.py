from flask import Blueprint, request, jsonify, g, current_app
from pypet import db
from pypet.models import Video
from werkzeug.utils import secure_filename
import os

bp = Blueprint('media', __name__, url_prefix='/media')  # 'video_upload' 블루프린트 생성

# 동영상 추가 라우트
@bp.route('/add', methods=['POST'])
def add_video():
    data = request.form  # 폼 데이터 가져오기
    title = data['title']  # 동영상 제목 가져오기
    content = data['content']  # 동영상 설명 가져오기
    video = request.files['video']  # 동영상 파일 가져오기
    username = data['username']
    
    if g.user is None:  # 사용자가 로그인되어 있지 않으면
        return jsonify({'error': 'Unauthorized'}), 401  # 인증 오류 반환
    
    video_filename = secure_filename(video.filename)  # 안전한 파일 이름 생성
    video_path = os.path.join(current_app.root_path, 'static', 'video_uploads', video_filename)  # 파일 경로 생성
    print(f"Video path: {video_path}")  # 경로 확인
    video.save(video_path)  # 파일 저장
    
    video_record = Video(  # 새로운 동영상 레코드 생성
        user_id=g.user.id,  # 사용자 ID 설정
        title=title,  # 제목 설정
        content=content,  # 설명 설정
        video_url=os.path.join('/static/video_uploads', video_filename), # 동영상 URL 설정
        username=username   
    )
    db.session.add(video_record)  # 데이터베이스에 추가
    db.session.commit()  # 변경사항 커밋
    
    return jsonify({'success': True, 'video_url': video_record.video_url})  # 성공 응답 반환

# 동영상 목록 조회 라우트
@bp.route('/list', methods=['GET'])
def list_videos():
    if g.user is None:  # 사용자가 로그인되어 있지 않으면
        return jsonify({'error': 'Unauthorized'}), 401  # 인증 오류 반환
    
    # videos = Video.query.filter_by(user_id=g.user.id).all()  # 사용자 ID로 동영상 목록 조회
    videos = Video.query.all()  # 동영상 목록 조회
    if g.user:
        username = g.user.username
    else:
        username = None
    video_list = [{  # 동영상 목록을 JSON 형식으로 변환
        'id': video.id,
        'title': video.title,
        'content': video.content,
        'video_url': video.video_url,
        'username': video.username,
        'login_user': username
    } for video in videos]
    
    return jsonify(video_list)  # 동영상 목록 반환

# 동영상 삭제 라우트
@bp.route('/delete/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    video = Video.query.get(video_id)  # 동영상 ID로 동영상 조회
    
    if video is None or video.user_id != g.user.id:  # 동영상이 없거나 사용자가 소유하지 않은 경우
        return jsonify({'error': 'Unauthorized'}), 401  # 인증 오류 반환
    
    
    db.session.delete(video)  # 데이터베이스에서 동영상 삭제
    db.session.commit()  # 변경사항 커밋
    
    return jsonify({'success': True})  # 성공 응답 반환

# 동영상 수정 라우트
@bp.route('/update/<int:video_id>', methods=['POST'])
def update_video(video_id):
    video = Video.query.get(video_id)  # 동영상 ID로 동영상 조회
    
    if video is None or video.user_id != g.user.id:  # 동영상이 없거나 사용자가 소유하지 않은 경우
        return jsonify({'error': 'Unauthorized'}), 401  # 인증 오류 반환
    
    # 제목과 내용 업데이트
    if 'title' in request.form:
        video.title = request.form['title']
    # if 'content' in request.form:
    #     video.description = request.form['content']
    data = request.form  # 폼 데이터 가져오기
    video.content = data['content']  # 동영상 설명 업데이트
    
    # 새로운 동영상 파일이 있는 경우
    if 'video' in request.files and request.files['video'].filename != '':
        video_file = request.files['video']
        video_filename = secure_filename(video_file.filename)
        video_path = os.path.join('static/video_uploads', video_filename)
        
        # 업로드 디렉토리가 없으면 생성
        if not os.path.exists('static/video_uploads'):
            os.makedirs('static/video_uploads')
        
        video_file.save(video_path)  # 파일 저장
        video.video_url = os.path.join('/static/video_uploads', video_filename)  # 동영상 URL 업데이트
    
    db.session.commit()  # 변경사항 커밋
    
    return jsonify({'success': True, 'video_url': video.video_url})  # 성공 응답 반환
