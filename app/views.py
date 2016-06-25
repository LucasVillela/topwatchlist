from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app,db,lm,bcrypt
from .models import Movie,Client,Watchlist
from .forms import LoginForm,RegisterForm

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	movies_watched = Movie.query.filter(Watchlist.movie_id == Movie.movie_id).filter(Watchlist.user_id == current_user.user_id).order_by(Movie.movie_id).all()
	movies_watched_id = Movie.query.with_entities(Movie.movie_id).filter(Watchlist.movie_id == Movie.movie_id).filter(Watchlist.user_id == current_user.user_id).all()
	movies = Movie.query.filter(~Movie.movie_id.in_(movies_watched_id)).order_by(Movie.movie_id).all()
	return render_template("index.html",movies=movies,movies_watched=movies_watched)

@app.route('/movie/<int:id>' , methods=['GET'])
@login_required
def movie(id):
	movie = Movie.query.filter_by(movie_id = id).first()
	return render_template("movie.html",movie=movie)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Client.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.passwd, form.password.data):
			login_user(user)
			return redirect(url_for('index'))
		flash('Wrong email or password')

	return render_template('login.html', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		checkuser = Client.query.filter_by(email = form.email.data).first()
		if checkuser:
			flash('User already exists')
			return redirect(url_for('register'))
		user = Client(form.nickname.data,form.dt_nasc.data,form.email.data,bcrypt.generate_password_hash(form.password.data))
		# user.nickname = form.nickname.data
		# user.dt_nasc = form.dt_nasc.data
		# user.email = form.email.data
		# user.passwd = bcrypt.generate_password_hash(form.password.data,getSalt())
		db.session.add(user)
		db.session.flush()
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html',form=form)

@app.route('/watched/<int:movie_id>', methods=['GET'])
def watched(movie_id):
	watchlist = Watchlist()
	watchlist.user_id = current_user.user_id
	watchlist.movie_id = movie_id
	watchlist.watch_id = watchlist.watch_id
	#watchlist = Watchlist(current_user.user_id, movie_id)
	db.session.add(watchlist)
	db.session.commit()

	return redirect(url_for('index'))

@app.route('/unwatched/<int:movie_id>', methods=['GET'])
def unwatched(movie_id):
	watchlist = Watchlist()
	Watchlist.query.filter(Watchlist.movie_id == movie_id).filter(Watchlist.user_id == current_user.user_id).delete()
	db.session.commit()

	return redirect(url_for('index'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@lm.user_loader
def load_user(user_id):
	return Client.query.get(user_id)


@app.before_request
def before_request():
	g.user = current_user