from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import usuario as Usu
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    if email == 'ADMIN':
        password = request.form.get('password')
    else:
        password = crip(request.form.get('password'))
    
    if email == 'ADMIN' and password == 'master@#99':
       existing_user = Usu.Usuario.query.filter_by(apelido=email).first()        
       if existing_user is None:
           user = Usu.Usuario(id_usuario=9999, 
                          senha='master@#99', 
                          apelido='ADMIN', 
                          nome='ADMINISTRADOR', 
                          adm='S', 
                          nivel=1)
           db.session.add(user)
           db.session.commit()  # Create new user    
        
    user = Usu.Usuario.query.filter_by(apelido=email).first()        
       
    if user is None:
        flash('Usuario nao encontrado verifique!')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    else:
        login_user(user, remember=False)
        if user.is_authenticated:
            return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = Usu.Usuario.query.filter_by(mailconta=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def crip(password):
    newpassword = ''
    for x in password:
        newpassword = newpassword + chr(~(ord(x) - 236)) 
    return newpassword
    