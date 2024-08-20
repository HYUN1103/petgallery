from flask import Blueprint, render_template

bp = Blueprint('hospmap', __name__, url_prefix='/hospmap')

@bp.route('/hosp')
def hosp():
    return render_template('hospmap/hosp.html')

