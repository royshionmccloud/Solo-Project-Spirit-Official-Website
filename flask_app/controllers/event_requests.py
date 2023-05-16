from flask_app import app
from flask import render_template,redirect,request,session, flash, url_for
from flask_app.models import spirit_user
from flask_app.models import event_request
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 



@app.route('/dashboard')
def sploginppro():
    if 'spirit_users_id' not in session:
        return redirect('/logout')
    user_spirit = spirit_user.Spirit_user.get_by_spirit_user_id({'id':session['spirit_users_id']})
    eventr=event_request.Event_request.get_all_event_request()
    return render_template('homepage.html', user_spirit=user_spirit, eventr=eventr)


@app.route('/new/event')
def add_event():
    if 'spirit_users_id' not in session:
        return redirect('/logout')
    user_spirit = spirit_user.Spirit_user.get_by_spirit_user_id({'id':session['spirit_users_id']})
    return render_template('requestevent.html', user_spirit=user_spirit)

@app.route('/create/event', methods=['POST'])
def pro_event():
    if 'spirit_users_id' not in session:
        return redirect('/logout')
    if not event_request.Event_request.spcheck(request.form):
            return redirect('/new/event')
    print(event_request.Event_request.save_request, "*"*20)

    data = {
        
        'name': request.form['name'],
        'location': request.form['location'],
        'event_date': request.form['event_date'],
        'details': request.form['details'],
        'spirit_users_id': session['spirit_users_id']
    }
    
    page_id = event_request.Event_request.save_request(data)
    return redirect(f'/event_request_review/{page_id}')

@app.route('/spiritbio')
def spirit_bio():
    if 'spirit_users_id' not in session:
        return redirect('/dashboard')

    return render_template('spiritbio.html')

# @app.route('/user/events')
# def user_events():
#     if 'spirit_users_id' not in session:
#         return redirect('/logout')
#     get_event = spirit_user.Spirit_user.all_spirit_user_events({'id':session['spirit_users_id']})
#     user = spirit_user.Spirit_user.get_by_spirit_user_id({'id':session['spirit_users_id']})
#     return render_template('viewevent.html', user=user, get_event=get_event)

@app.route('/event_request_review/<int:id>')
def view_events(id):
    if 'spirit_users_id' not in session:
        return redirect('/logout')
    print()
    event_review = event_request.Event_request.get_user_one_event_request({'id': id})
    user_spirit = spirit_user.Spirit_user.get_by_spirit_user_id({'id':session['spirit_users_id']})
    return render_template('viewevent.html', user_spirit=user_spirit, event_review=event_review )

@app.route('/requestconfirmed')
def confirm_event():
    if 'spirit_users_id' not in session:
        return redirect('/dashboard')
    user_spirit = spirit_user.Spirit_user.get_by_spirit_user_id({'id':session['spirit_users_id']})
    return render_template('pgsubmitted.html', user_spirit=user_spirit)

@app.route('/edit_event_request/<int:id>')
def edit_event(id):
    if 'spirit_users_id' not in session:
        return redirect('/logout')
    user_spirit = spirit_user.Spirit_user.get_by_spirit_user_id({'id':session['spirit_users_id']})
    return render_template('editevent.html', editevent=event_request.Event_request.get_user_one_event_request({'id': id}), user_spirit=user_spirit)


@app.route('/edit_event_request/<int:id>/process', methods=['POST'])
def process_edit_event(id):
    if 'spirit_users_id' not in session:
        return redirect('/logout')
    if not event_request.Event_request.spcheck(request.form):
        return redirect('/edit_event_request')

    data = {
        'id': id,
        'name': request.form['name'],
        'location': request.form['location'],
        'event_date': request.form['event_date'],
        'details': request.form['details']
    }
    event_request.Event_request.update_request(data)
    return redirect(f'/event_request_review/{id}')

@app.route('/destroy/<int:id>')
def destroy_event_request(id):
    if 'spirit_users_id' not in session:
        return redirect('/logout')

    event_request.Event_request.destroy_event({'id':id})
    flash("Event Successfully Deleted") 
    return redirect('/dashboard')