from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, EmailField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Length, Regexp
from datetime import datetime
from bdd_requests import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKey'


rooms = [(room['id_room'], f"{room['room_type']} - {room['price_per_night'][:-3]} NTD/night ({room['max_guests']} p. max)") for room in get_rooms()['data']] if get_rooms()['success'] else []


date = datetime.now()

class BookingForm(FlaskForm):
    room_number = SelectField('Room Number', choices=rooms, validators=[DataRequired()])
    check_in_date = DateField('Check-In Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out_date = DateField('Check-Out Date', format='%Y-%m-%d', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = StringField('Password', widget=PasswordInput(), validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    phone_number = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex='^[0-9]+$')])
    submit = SubmitField('Sign up')
    
class LogInForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = StringField('Password', widget=PasswordInput(), validators=[DataRequired()])
    submit = SubmitField('Log in')

# def error():
#     response = get_rooms()
#     if not response['success']:
#         raise Exception(response['error'])

# @app.errorhandler(500)
# def handle_error(e):
#     return render_template('404.html', error=str(e)), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    session['date'] = date.strftime("%Y-%m-%d")
    form=BookingForm()
    if form.validate_on_submit():
            
        if form.check_in_date.data > form.check_out_date.data or form.check_in_date.data < datetime.today().date():
            return render_template('index.html', form=form, error="Check-in or Check-out date not valid !")
        
        if 'id_guest' in session:
            response = book_room(session['id_guest'],form.room_number.data, form.check_in_date.data.strftime('%Y-%m-%d'), form.check_out_date.data.strftime('%Y-%m-%d'))
        else:
            return render_template('index.html', form=form, error="You are not connected !")
            
        if response['success']:
            return redirect(url_for('mybookings'))
        else:
            return render_template('index.html', form=form, error=response['error'])

    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        response = log_in(form.email.data, form.password.data)
        # print(response['data'])
        if response['success']:
            session['id_guest'] = response['data']['id_guest'] 
            print(f"id_guest : {session['id_guest']}")
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=form, error=response['error'])
            
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        response = sign_up(form.email.data, form.password.data, form.last_name.data, form.first_name.data, form.phone_number.data)
        if response['success']:
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', form=form, error=response['error'])
    return render_template('signup.html', form=form)

@app.route('/mybookings')
def mybookings():
    response = get_bookings(session['id_guest'])
    # print(response['data'])
    if response['success']:
        return render_template('mybookings.html', data=response['data']['bookings'], rooms={room[0]: room[1] for room in rooms})
    else:
        return render_template('mybookings.html', error=response['error'])
        

@app.route('/logout')
def logout():
    session.pop('id_guest', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)