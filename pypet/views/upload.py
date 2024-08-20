from flask import Blueprint, render_template


bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/video')
def video():
    return render_template('upload/video.html')
