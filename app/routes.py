from flask import render_template,flash,redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddWordForm, EditProfileForm, DictionaryForm
from app.models import User, Word, Language, Dictionary
from app.translate import translate
from guess_language import guess_language
import random
from flask_babel import _

@app.route('/')
@app.route('/index')
@login_required
def index():
	NEWSAPI = app.config['NEWSAPI']
	
	language = Language.query.filter_by(id = current_user.language_id).first().lit

	newsapi = NEWSAPI.get_top_headlines(country="ru")
	return render_template('index.html', title='Home'  , user = current_user.username, newsapi = newsapi['articles']  )

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
	#form.languages.choices = [(language.id, language.language) for language in Language.query.all()]
	form.languages1.choices = [(language.id, language.language) for language in Language.query.all()]
	if form.validate_on_submit():
		language = Language.query.filter_by(id=form.my_language.data).first()	
		user = User(username = form.username.data, email=form.email.data, language_id=language.id)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		foreign_languages = form.languages1.data
		for foreign_language in foreign_languages:
			language = Language.query.filter_by(id=foreign_language).first()
			dictionary = Dictionary(user_id=user.id, language_id=language.id)
			db.session.add(dictionary)
			db.session.commit()
		flash(_('Congratulations, you are now a registered user!'))
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form = form)

@app.route('/mywords/',methods=['GET','POST'])
@login_required
def mywords():
	dictionaryForm = DictionaryForm()
	dictionaries = current_user.languages
	languages_id = [language.language_id for language in dictionaries]
	languages = [Language.query.filter_by(id=language_id).first() for language_id in languages_id]
	dictionaryForm.foreign_languages.choices = [(language.id, language.language) for      language in  languages]
	page = request.args.get('page',1,type=int)
	if dictionaryForm.validate_on_submit():
		languageid = dictionaryForm.foreign_languages.data
		language = Language.query.filter_by(id = languageid).first()
		words = current_user.languages.filter_by(language_id = language.id).first().words.paginate(
		page, app.config['WORDS_PER_PAGE'], False)
		foreign_languages = current_user.languages
		next_url = url_for('mywords',page = words.next_num) \
		if words.has_next else None
		previous_url = url_for('mywords', page = words.prev_num) \
		if words.has_prev else None  
		return render_template('mywords.html',title = 'Dictionary', words = words.items, next_url = next_url , previous_url = previous_url, form=dictionaryForm)
	else:

		language_id=0
		words = current_user.languages[language_id].words.paginate(
			page, app.config['WORDS_PER_PAGE'], False)
		foreign_languages = current_user.languages
		next_url = url_for('mywords',page = words.next_num) \
		if words.has_next else None
		previous_url = url_for('mywords', page = words.prev_num) \
		if words.has_prev else None  
		return render_template('mywords.html',title = 'Dictionary', words = words.items, next_url = next_url , previous_url = previous_url, form=dictionaryForm)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	languages = Language.query.all()
	form.languages.choices = [(language.id, language.language) for language in languages]
	if form.validate_on_submit():
		languages_id = [dictionary.language_id for dictionary in current_user.languages]
		if form.languages.data not in languages_id:

			current_user.username = form.username.data
			language_id = form.languages.data

			user_new_dictionary = Dictionary(user_id = current_user.id, language_id = language_id)
			db.session.add(user_new_dictionary)
			db.session.commit()
			dictionary = Dictionary(user_id = current_user.id, language_id = form.languages.data)
			flash(_('Your changes have been saved!'))
			return redirect(url_for('edit_profile'))
		else:
			flash('The chosen language is alreay in your dictionary')
	return render_template('edit_profile.html', title='Edit Profile', form = form)

@app.route('/search')
@login_required
def search():
	form = AddWordForm()
	dictionaries = current_user.languages
	languages_id = [language.language_id for language in dictionaries]
	languages = [Language.query.filter_by(id=language_id).first() for language_id in languages_id]
	form.languages.choices = [(language.id, language.language) for language in languages]
	return render_template('search.html', title = 'Search', form=form )

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


@app.route('/get_languages', methods=['GET', 'POST'])
@login_required
def get_langauges():
	languages = [{'lit': language.lit, 'language': language.language} for language in Language.query.all()]
	return jsonify({'languages': languages})

@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
	return jsonify({'text': translate(request.form['text'],request.form['destLanguage'], request.form['sourceLanguage'])})

@app.route('/add_word', methods=['POST'])
@login_required
def add_word():
	word = Word(native_language = request.form['text'], foreign_language = request.form['translation'], dictionary_id =Dictionary.query.filter_by(language_id=Language.query.filter_by(lit=request.form['foreign_Language']).first().id).filter_by(user_id = current_user.id).first().id)
	db.session.add(word)
	db.session.commit()
	flash(_('The word has been added in the dictionary ! '))
	return render_template('search.html', title='Search')
	
    
@app.route('/get5words', methods=['POST','GET'])
@login_required
def get5words():
	words = Word.query.filter_by(user_id = current_user.id).limit(5).all()
	return jsonify(words = [e.serialize() for e in words])



@app.route('/game_true_false')
@login_required
def game_true_false():
	return render_template('game_true_false.html', title='True or False')
	



@app.route('/get_words', methods=['POST', 'GET'])
@login_required
def get_words():
	words = [word for word in dictionary for dictionaries in current_user.languages.all()]
	i = random.randint(0,len(words)-1)
	j = random.randint(0,len(words)-1)
	#user_words = Word(foreign_language=user_words_repeats[i].foreign_language, native_language = user_words_repeats[j].native_language, native_language_true = user_words_repeats[i].native_language)
	user_word = {
		"foreign_language": user_words_repeats[i].foreign_language,
		"native_language": user_words_repeats[j].native_language,
		"native_language_true": user_words_repeats[i].native_language
	}
	if i==j:
		answer=1
	else:
		answer=2
	return jsonify({"words": {"foreign_language": user_words_repeats[i].foreign_language,
							 "native_language": user_words_repeats[j].native_language,
								"native_language_true": user_words_repeats[i].native_language},
					"answer":	answer})    

@app.route('/associate_game')
@login_required
def associate_game():
	words = Word.query.filter_by(user_id = current_user.id).limit(7).all()
	return render_template('associate_game.html', title='Associate Game1234', words = words)

@app.route('/clear/word/<id>')
@login_required
def update_words():
	language = Language.query.all()
	user = User.query.all()



@app.route('/words_errors', methods=['POST','GET'])
@login_required
def get_words_errors_games():
	words_answer = request.form['words']
	words_result = words_answer
	return render_template('word_errors.html', title='Word Errors', words_answer=words_result)


@app.route('/initPage', methods=['POST','GET'])
@login_required
def initPage():
	languages = [{'en': 'English', 'ru': 'Russian', 'fr': 'French', 'it': 'Italian'}]
	return jsonify({'lang':languages})














