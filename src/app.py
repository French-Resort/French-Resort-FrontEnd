from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime
from markupsafe import Markup
import html

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


@app.route('/', methods=['GET', 'POST'])
def index():
    form=BookingForm()
    if form.validate_on_submit():
        if form.check_in_date.data > form.check_out_date.data or form.check_in_date.data < datetime.today().date():
            return render_template('index.html', form=form, error="Check-in or Check-out date not valid !")

    return render_template('index.html', form=form)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signin():
    return render_template('signup.html')

@app.route('/mybookings')
def mybookings():
    return render_template('mybookings.html')



if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)