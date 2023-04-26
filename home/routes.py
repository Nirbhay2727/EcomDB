from flask import render_template,flash,redirect,url_for,request
from home.forms import RegistrationForm,LoginForm,UpdateAccountForm,RequestResetForm,ResetPasswordForm
from home.models import User,Product
from flask_login import login_user,current_user,logout_user,login_required
from home import app, db, bcrypt,mail
from flask_mail import Message


products = [
    {
        'name':'Item 1',
        'cost':24.00,
        'category':'category 1',
        'brand':'brand 1',
        'retail_price':26.00,
        'department':'department 1',
        'sku':'sku 1',
        'distribution_center_id':'distribution_center_id 1'

    }
]


@app.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    products=Product.query.paginate(per_page=10,page=page)
    return render_template('home.html',title='Home',products=products)

@app.route("/signup",methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()

    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.first_name.data}! Please login below.','success')
        return redirect(url_for('login'))
    return render_template('signup.html',title='Sign Up',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash('You have been logged in!','success')
            return  redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/account",methods=['GET','POST'])
@login_required
def account(): 
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name=form.first_name.data
        current_user.last_name=form.last_name.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.first_name.data=current_user.first_name
        form.last_name.data=current_user.last_name
        form.email.data=current_user.email

    return render_template('account.html',title='Account',form=form)


@app.route("/logout")
def logout():
    logout_user() 
    return redirect(url_for('home'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)