import os
from cocktails_site import app, db
from flask import render_template, redirect, url_for, flash, request
from cocktails_site.models import User, Cocktail, Ingredient
from cocktails_site.forms import RegisterForm, LoginForm, AddCocktailForm
from flask_login import login_user, logout_user, login_required, current_user, user_logged_in
from werkzeug.utils import secure_filename
from sqlalchemy import or_


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/library')
def library():
    if current_user.is_authenticated:
        cocktails = Cocktail.query.filter(
            or_(Cocktail.is_user_cocktail == False, (Cocktail.user_id == current_user.id) &
                (Cocktail.is_user_cocktail == True))).all()
    else:
        # If user is not authenticated, query only non-user cocktails
        cocktails = Cocktail.query.filter_by(is_user_cocktail=False).all()

    return render_template('library.html', cocktails=cocktails)


@app.route('/library/<cocktail>')
def cocktail(cocktail):
    cocktail = Cocktail.query.filter_by(name=cocktail).first()
    return render_template('cocktail.html', cocktail=cocktail)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        return redirect(url_for('library'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(error, category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            return redirect(url_for('library'))
        else:
            flash('Username or password incorrect!', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('home'))


@app.route('/add-cocktail', methods=['GET', 'POST'])
@login_required
def add_cocktail():
    form = AddCocktailForm()
    if form.validate_on_submit():
        file = form.image.data
        secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], form.name.data.replace(' ', '_') + file.filename[-4:]))

        cocktail = Cocktail(name=form.name.data, description=form.description.data, user_id=current_user.id)
        db.session.add(cocktail)
        db.session.commit()

        return redirect(url_for('library'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(error, category='danger')

    return render_template('add_cocktail.html', form=form)
