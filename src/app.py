from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, EmailField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Length, Regexp
from datetime import datetime
import requests
from bdd_requests import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKey'

# Retrieve rooms from the database
def updateRoomsChoice():
    return [(room['id_room'], f"{room['room_type']} - {room['price_per_night'][:-3]} NTD/night ({room['max_guests']} p. max)") for room in get_rooms()['data']] if get_rooms()['success'] else []


# Current date
today = datetime.today().date()

class BookingForm(FlaskForm):
    """
    Form for booking a room.

    Attributes:
    - room_number (SelectField): Dropdown list for selecting a room.
    - check_in_date (DateField): Field for entering the check-in date.
    - check_out_date (DateField): Field for entering the check-out date.
    """
    room_number = SelectField('Room Choices', choices=updateRoomsChoice(), validators=[DataRequired()])
    check_in_date = DateField('Check-In Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out_date = DateField('Check-Out Date', format='%Y-%m-%d', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    """
    Form for user sign-up.

    Attributes:
    - email (EmailField): Field for entering the email address.
    - password (StringField): Field for entering the password.
    - last_name (StringField): Field for entering the last name.
    - first_name (StringField): Field for entering the first name.
    - phone_number (StringField): Field for entering the phone number.
    - submit (SubmitField): Button for submitting the form.
    """
    email = EmailField('Email', validators=[DataRequired()])
    password = StringField('Password', widget=PasswordInput(), validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    phone_number = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex='^[0-9]+$')])
    submit = SubmitField('Sign up')

class LogInForm(FlaskForm):
    """
    Form for user log-in.

    Attributes:
    - email (EmailField): Field for entering the email address.
    - password (StringField): Field for entering the password.
    - submit (SubmitField): Button for submitting the form.
    """
    email = EmailField('Email', validators=[DataRequired()])
    password = StringField('Password', widget=PasswordInput(), validators=[DataRequired()])
    submit = SubmitField('Log in')

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page route for booking a room.

    Returns:
    - render_template: Renders the 'index.html' template.
    """
    session['today'] = today.strftime("%Y-%m-%d")
    form = BookingForm()
    if form.validate_on_submit():
        if form.check_in_date.data > form.check_out_date.data or form.check_in_date.data < datetime.today().date():
            return render_template('index.html', form=form, error="Check-in or Check-out date not valid !")

        if 'id_guest' in session:
            response = book_room(session['id_guest'], form.room_number.data, form.check_in_date.data.strftime('%Y-%m-%d'), form.check_out_date.data.strftime('%Y-%m-%d'))
        else:
            return render_template('index.html', form=form, error="You are not connected !")

        if response['success']:
            # return redirect(url_for('mybookings'))
            return render_template('index.html', form=form, success=True)
        else:
            return render_template('index.html', form=form, error=response['error'])

    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page route for user log-in.

    Returns:
    - render_template: Renders the 'login.html' template.
    """
    form = LogInForm()
    if form.validate_on_submit():
        response = log_in(form.email.data, form.password.data)
        if response['success']:
            session['id_guest'] = response['data']['id_guest']
            print(f"id_guest : {session['id_guest']}")
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=form, error=response['error'])

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up page route for user registration.

    Returns:
    - render_template: Renders the 'signup.html' template.
    """
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
    """
    My Bookings page route to display user bookings.

    Returns:
    - render_template: Renders the 'mybookings.html' template.
    """
    response = get_bookings(session['id_guest'])
    if response['success']:
        # print(response['data']['bookings'])
        total_spent = 0
        # CALCULATE TOTAL SPENT
        for booking_data in response['data']['bookings']:
            total_price_str = booking_data.get("total_price", "0.0")  # Get the total_price value or default to "0.0"

            try:
                total_price_double = float(total_price_str)
                total_spent = total_spent + total_price_double
            except ValueError:
                # Handle the case where conversion to double is not possible
                print(f"Error converting total_price for booking ID {booking_data['id_booking']}")
        return render_template('mybookings.html', data=response['data']['bookings'], rooms={room[0]: room[1] for room in updateRoomsChoice()}, total_spent=total_spent)
    else:
        return render_template('mybookings.html', error=response['error'])

@app.route('/logout')
def logout():
    """
    Logout route to log out the user.

    Returns:
    - redirect: Redirects to the 'index' route.
    """
    session.pop('id_guest', None)
    return redirect(url_for('index'))


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
