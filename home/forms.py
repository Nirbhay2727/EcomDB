from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import Length,DataRequired,Email,EqualTo,ValidationError
from home.models import User

class RegistrationForm(FlaskForm):
    first_name =StringField('First Name',validators=[DataRequired(),Length(min=2,max=20)])
    last_name =StringField('Last Name',validators=[DataRequired(),Length(min=2,max=20)])
    email =StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose another one.')


class LoginForm(FlaskForm):
    email =StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name =StringField('First Name',validators=[DataRequired(),Length(min=2,max=20)])
    last_name =StringField('Last Name',validators=[DataRequired(),Length(min=2,max=20)])
    email =StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Update Info')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose another one.')


class RequestResetForm(FlaskForm):
    email =StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request Password Reset')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register first.')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Reset Password')