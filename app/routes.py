from flask import render_template,flash,redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddWordForm, EditProfileForm
from app.models import User, Word, Language, Dictionary
from app.translate import translate
from flask_babel import _



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
			flash(_('Invalid username or password'))
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
	form.my_language.choices = [(language.id, language.language) for language in Language.query.all()]
	form.languages.choices = [(language.id, language.language) for language in Language.query.all()]
	if form.validate_on_submit():
		language = Language.query.filter_by(language=form.my_language.data).first().id
		foreign_languages = Language.query.filter_by(language=form.languages.data).first().id
		user = User(username = form.username.data, email=form.email.data, language_id=language)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		dictionary = Dictionary(user_id=current_user.id, language_id=foreign_languages)
		db.session.add(dictionary)
		db.session.commit()
		flash(_('Congratulations, you are now a registered user!'))
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form = form)

@app.route('/mywords',methods=['GET','POST'])
@login_required
def mywords():
	page = request.args.get('page',1,type=int)
	words = current_user.languages[0].words.paginate(
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
		flash(_('Your changes have been saved!'))
		return redirect(url_for('edit_profile'))
	return render_template('edit_profile.html', title='Edit Profile', form = form)

@app.route('/search')
@login_required
def search():
	return render_template('search.html', title = 'Search' )

@app.route('/games')
@login_required
def games():
	return render_template('games.html',title = 'Games')



@app.route('/yes_not')
@login_required
def yes_not():
	return render_template('yes_not.html',title = 'Yes or Not')



@app.route('/getNext', methods=['POST','GET'])
@login_required
def getNext():
	words = Word.query.filter_by(user_id = current_user.id).all()
	return jsonify(words = [e.serialize() for e in words])



@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
	return jsonify({'text': translate(request.form['text'],request.form['sourcelang'],request.form['destlang'])})

@app.route('/add_words', methods=['POST'])
@login_required
def add_wordsx():
	word = Word(english = request.form['eng'], russian = request.form['russian'] , remarks = request.form['remarks'],     user_id = current_user.id)
	db.session.add(word)
	db.session.commit()
	flash(_('The word has been added in the dictionary ! '))
	return render_template('search.html', title='Search')
	

@app.route('/get5words', methods=['POST','GET'])
@login_required
def get5words():
	words = Word.query.filter_by(user_id = current_user.id).limit(5).all()
	return jsonify(words = [e.serialize() for e in words])



@app.route('/associate_game')
@login_required
def associate_game():
	words = Word.query.filter_by(user_id = current_user.id).limit(5).all()
	return render_template('associate_game.html', title='Associate Game', words = words)


@app.route('/initPage', methods=['POST','GET'])
@login_required
def initPage():
	languages = [{'en': 'English', 'ru': 'Russian', 'fr': 'French', 'it': 'Italian'}]
	return jsonify({'lang':languages})










