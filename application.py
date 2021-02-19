from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response
	
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ---------- database configuration -----------------
import sqlite3, os
from flask import g

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
		
DATABASE = 'database.db'
if not os.path.isfile(DATABASE):
	# create database from schema if necessary
	init_db()

@app.route("/")
def index():
	'''homepage - simply renders existing db state
	'''
	
	return render_template('index.html', entries=['a','b','c'])
	
@app.route("/register", methods=["GET", "POST"])
def register():
	'''Allows user to register for an account
	'''
	
	# Forget any user_id
	session.clear()

	# User submitted form
	if request.method == "POST":

		# Ensure username was submitted
		if not request.form.get("username"):
			# to-do: produce error message of some kind
			return redirect('/register')

		# Ensure password was submitted
		elif not request.form.get("password"):
			# to-do: produce error message of some kind
			return redirect('/register')

		# TO-DO: store username/hashed passwords in DB
		try:
			db = get_db()
			cur = db.cursor()
			cur.execute('''INSERT INTO users (username,hash) 
			   VALUES (?,?)''',(request.form.get("username"), request.form.get("password")))
			
			db.commit()
		except:
			db.rollback()
         
		# Remember which user has logged in
		#session["user_id"] = rows[0]["id"]

		# Redirect user to home page
		return redirect("/")

	# User reached route via GET (as by clicking a link or via redirect)
	else:
		return render_template("register.html")