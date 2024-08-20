from flask import Blueprint, render_template

bp = Blueprint('gallery', __name__, url_prefix='/gallery')

@bp.route('/photo')
def photo():
    return render_template('gallery/photo.html')

