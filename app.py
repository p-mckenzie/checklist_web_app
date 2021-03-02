from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
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
    db = get_db()
    cur = db.cursor()
    
    rows = cur.execute('''select username from users;''').fetchall()
    
    return render_template('index.html', entries=[row[0] for row in rows])
    
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

        try:
            db = get_db()
            cur = db.cursor()
            
            rows = cur.execute('''select username from users where username = ?;''', 
                            [request.form.get("username")]).fetchall()
            if len(rows)>0:
                # to-do: produce error message of some kind
                return redirect('/register')
                        
            # to-do: actually secure hash
            cur.execute('''INSERT INTO users (username,hash) 
               VALUES (?,?)''', [request.form.get("username"), hash(request.form.get("password"))])
            
            db.commit()
            
            rows = cur.execute('''select username from users where username = ?;''', 
                            [request.form.get("username")]).fetchall()
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            return redirect('index')
            
        except:
            db.rollback()
            # to-do: produce error message of some kind
            return redirect('/register')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
        
@app.route("/login", methods=["GET", "POST"])
def login():
    '''Allows user to register for an account
    '''
    
    # Forget any user_id
    session.clear()

    # User submitted form
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            # to-do: produce error message of some kind
            return redirect('/login')

        # Ensure password was submitted
        elif not request.form.get("password"):
            # to-do: produce error message of some kind
            return redirect('/login')

        # TO-DO: store username/hashed passwords in DB
        try:
            db = get_db()
            cur = db.cursor()
            row = cur.execute('''select hash,id from users where username = ?;''', 
                            [request.form.get("username")]).fetchall()[0]
            
            # check password
            print(row[0])
            # to-do: actually secure hash
            if row[0]!=hash(request.form.get("password")):
                print("wrong password")
                return redirect('/login')
            else:            
                # Remember which user has logged in
                session["user_id"] = row[1]
        except:
            print('whoop')
            return redirect('/login')
                
        # Redirect user to home page
        print('redirecting')
        return redirect('index')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")