from flask import Blueprint, render_template 
from flask_login import login_required, current_user
import redmine as rm

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@login_required
def index():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        
        return render_template('index.html', name=current_user.apelido,is_authenticated=current_user.is_authenticated)

@main.route('/redmine_atendimento')
def redmine_atendimento():
    rm.rel_atendimento()
    return render_template('redmine_atendimento.html')    
