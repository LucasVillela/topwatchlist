from app import db



class Client(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(120))
	dt_nasc = db.Column(db.Date)
	email = db.Column(db.String(55))
	passwd = db.Column(db.String(30))

	def __repr__(self):
		return '<Client %r>' % (self.nickname)

	def __init__(self, nickname, dt_nasc,email,passwd):
		self.nickname = nickname
		self.dt_nasc = dt_nasc
		self.email = email
		self.passwd = passwd

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.user_id)  # python 2
		except NameError:
			return str(self.user_id)  # python 3

class Movie(db.Model):
	movie_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	imdb_rating = db.Column(db.String(10))
	overview = db.Column(db.String(255))
	poster = db.Column(db.String(60))
	release_date = db.Column(db.String(20))
	awards = db.Column(db.String(100))
	actors = db.Column(db.String(255))

	def __repr__(self):
		return '<Movie %r>' % (self.title)

class Watchlist(db.Model):
	user_id = db.Column(db.Integer)
  	movie_id = db.Column(db.Integer)
  	watch_id = db.Column(db.Integer, primary_key=True)

  	#db.ForeignKey('Client.user_id')
  	#db.ForeignKey('Movie.movie_id')

  	
