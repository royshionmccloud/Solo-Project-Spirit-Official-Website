from flask_app import app
from flask import render_template,redirect,request,session, flash
from flask_app.models import spirit_user
from flask_app.models import event_request
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)



@app.route('/')
def index_spirit():
    return redirect('/login')

@app.route('/login')
def spirit_login():
    if 'spirit_users_id' in session:
        return redirect('/dashboard')

    return render_template('logspirit.html')

@app.route('/spirit_login', methods=['POST'])
def spirit_login_pro():
    data = { "email" : request.form["email"] }
    users_sp = spirit_user.Spirit_user.get_by_spirit_user_email(data)
    if not users_sp:
        flash("Invalid Email/Password") 
        return redirect('/login')
    if not bcrypt.check_password_hash(users_sp.password, request.form['password']):
        flash("Invalid Email/Password") 
        return redirect('/')
    session['spirit_users_id'] = users_sp.id
    return redirect('/dashboard')

@app.route('/spirit_register', methods=['POST'])
def register_check():
    if not spirit_user.Spirit_user.validate_spirit_reg(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'].lower(),
        "last_name": request.form['last_name'].lower(),
        "email": request.form['email'].lower(),
        "password" : pw_hash
    }
    user_id = spirit_user.Spirit_user.save_reg_spirit_u(data)
    session['spirit_users_id'] = user_id
    return redirect("/dashboard")

@app.route('/logout')
def logout_spirit_page():
    session.clear()
    return redirect('/')