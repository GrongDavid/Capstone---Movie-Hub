from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('Profile image (leave blank if none)')