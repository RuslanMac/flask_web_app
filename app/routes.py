from flask import render_template,flash,redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddWordForm, EditProfileForm
from app.models import User, Word
from app.translate import translate



@app.route('/')
@app.route('/index')
@login_required
def index():

	return render_template('index.html', title='Home'  , user = current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html',title='Sign In',form=form)

@app.route('/register', methods = ['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username = form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form = form)

@app.route('/mywords',methods=['GET','POST'])
@login_required
def mywords():
	page = request.args.get('page',1,type=int)
	words = current_user.words.paginate(
		page, app.config['WORDS_PER_PAGE'], False)
	next_url = url_for('mywords',page = words.next_num) \
	if words.has_next else None
	previous_url = url_for('mywords', page = words.prev_num) \
	if words.has_prev else None
	return render_template('mywords.html',title = 'Dictionary', words = words.items, next_url = next_url , previous_url = previous_url)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.language = form.language.data
		db.session.commit()
		flash('Your changes have been saved!')
		return redirect(url_for('edit_profile'))
	return render_template('edit_profile.html', title='Edit Profile', form = form)


@app.route('/search', methods = ['GET','POST'])
@login_required
def search():
	
	return render_template('search.html', title = 'Search')

@app.route('/games')
@login_required
def games():
	return render_template('games.html',title = 'Games')

@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
	return jsonify({'text': translate(request.form['text'])})























