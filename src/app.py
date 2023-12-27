from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, ValidationError, InputRequired, Email, Length, Regexp
from datetime import datetime
from markupsafe import Markup
import html
from bdd_requests import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKey'

rooms = [
    ('101', 'Single Room'),
    ('102', 'Double Room'),
    ('103', 'Deluxe Room')
]



class BookingForm(FlaskForm):
    room_number = SelectField('Room Number', choices=rooms, validators=[DataRequired()])
    check_in_date = DateField('Check-In Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out_date = DateField('Check-Out Date', format='%Y-%m-%d', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', widget=PasswordInput(), validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex='^[0-9]+$')])
    submit = SubmitField('Sign Up')
    
class LogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', widget=PasswordInput(), validators=[DataRequired()])
    submit = SubmitField('Log In')


@app.route('/', methods=['GET', 'POST'])
def index():
    form=BookingForm()
    if form.validate_on_submit():
        if form.check_in_date.data > form.check_out_date.data or form.check_in_date.data < datetime.today().date():
            return render_template('index.html', form=form, error="Check-in or Check-out date not valid !")
        
        # if check_rooms_available():
        #     return render_template('index.html', form=form, error="Rooms are available !")
        
        book_room(1,form.room_number.data, form.check_in_date.data.strftime('%Y-%m-%d'), form.check_out_date.data.strftime('%Y-%m-%d'))
        

    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        log_in(form.email.data, form.password.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        sign_up(form.email.data, form.password.data, form.last_name.data, form.first_name.data, form.phone_number.data)
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/mybookings')
def mybookings():
    return render_template('mybookings.html')



if __name__ == '__main__':
    bdd_init()
    app.run(host="localhost", port=5000, debug=True)