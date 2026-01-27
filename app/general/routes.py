from flask import Blueprint, render_template
from flask_login import login_required

general = Blueprint('general', __name__)

@general.route('/menu')
@login_required
def menu():
    return render_template('general/menu.html')
