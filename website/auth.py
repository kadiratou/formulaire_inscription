from flask import Blueprint, render_template,request,flash,url_for,redirect
from .models import User,Note,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required,login_user,current_user,logout_user
from . import db




auth = Blueprint('auth', __name__)


@auth.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('connexion réussie', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('mot de passe incorrect.', category='error')
        else:
            flash('ce mail n\'existe pas.', category='error')
    return  render_template("login.html", user=current_user)


@auth.route('/sign_up',methods=["GET","POST"])
def sign_up():
    if request.method=='POST':
        email =request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        user = User.query.filter_by(email=email).first()

        if user:
            flash('le mail existe deja', category='error')
        if len(email) < 4 :
            flash('le mail doit avoir plus de 3 caractères  .',category='error')
        elif len(firstName) < 2:
            flash('le nom doit avoir plus de 1 caractères .',category='error')
        elif password1 != password2:
            flash(' les mots de passe sont différents',category='error')
        elif len(password1) < 7:
            flash('le mot de passe doit avoir plus de 6 caractères .',category='error')
        else:
            new_user=User(email=email, firstName=firstName , password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('compte cré ',category='success')
            return redirect(url_for('views.home'))
            #add user to database

    return render_template("sign_up.html",user=current_user)


@auth.route('/logout',methods=["GET","POST"])

def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    return  render_template("logout.html")
