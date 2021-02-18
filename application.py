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

		# Remember which user has logged in
		#session["user_id"] = rows[0]["id"]

		# Redirect user to home page
		return redirect("/")

	# User reached route via GET (as by clicking a link or via redirect)
	else:
		return render_template("register.html")