from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app,db,lm,oid
from .models import Movie,Client,Watchlist
from .forms import LoginForm

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	movies_watched = Movie.query.filter(Watchlist.movie_id == Movie.movie_id).filter(Watchlist.user_id == current_user.user_id).order_by(Movie.movie_id).all()
	#movies_watched_id = Watchlist.query(Watchlist.movie_id).filter(Watchlist.user_id == current_user.user_id).all()
	#movies_watched_id = db.engine.execute("SELECT movie_id from watchlist where user_id = 2")
	movies_watched_id = Movie.query.with_entities(Movie.movie_id).filter(Watchlist.movie_id == Movie.movie_id).filter(Watchlist.user_id == current_user.user_id).all()
	movies = Movie.query.filter(~Movie.movie_id.in_(movies_watched_id)).order_by(Movie.movie_id).all()
	#movies = Movie.query.order_by(Movie.movie_id).all()
	#watchlist = Watchlist.query.filter_by(user_id = user.user_id).all()
	return render_template("index.html",movies=movies,movies_watched=movies_watched)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		flash(form.email.data)
		user = Client.query.filter_by(email = form.email.data).first()
		if user:
			login_user(user)
			return redirect(url_for('index'))

	return render_template('login.html', form=form)


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