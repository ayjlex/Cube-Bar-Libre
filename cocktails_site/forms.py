from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from cocktails_site.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists.')

    username = StringField(label='Username :', validators=[Length(min=3, max=30), DataRequired()])
    password = PasswordField(label='Password :', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password :', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username :', validators=[DataRequired()])
    password = PasswordField(label='Password :', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class AddCocktailForm(FlaskForm):
    name = StringField(label='Cocktail Name :', validators=[Length(max=30), DataRequired()])
    description = StringField(label='Description :', validators=[Length(min=20, max=700), DataRequired()])
    image = FileField(label='Image :', validators=[FileRequired(), FileAllowed(['jpg'])])
    submit = SubmitField(label='Add')
