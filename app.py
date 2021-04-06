from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session

from tempfile import mkdtemp
import datetime

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
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
DATABASE = 'database.db'
#if not os.path.isfile(DATABASE):
    # create database from schema if necessary
os.remove(DATABASE)
init_db() # for testing - always reset database
    
def hash(str):
    return ord(str[0])

@app.route("/", methods=['GET', 'POST'])
def index():
    '''homepage - renders existing tasks for user & allows them to mark them as complete
    '''
    
    # for testing - avoids having to log in as "test" user each time
    session['user_id'] = 1
    db = get_db()
    cur = db.cursor()
    
    if request.method == "POST":     
        # update database to mark current task complete
        if len(request.form)>0:
            # current task complete
            cur.execute('''UPDATE tasks SET complete=(CASE WHEN complete=0 then 1 else 0 end) where id=?;''', [list(request.form)[0]])
            db.commit()
            
            try:
                # if it repeats, create next instance
                row = dict(cur.execute('''select *, case when freq=1 then date(date,'+1 days') 
                                                        when freq=2 then date(date,'+7 days') 
                                                        when freq=3 then date(date,'+1 months') 
                                                        when freq=4 then date(date,'+1 years') 
                                                        end as next_date 
                                    from tasks
                                    where id=? and freq>0;''', 
                        [list(request.form)[0]]).fetchall()[0])
                
                cur.execute('''INSERT INTO tasks (user_id,title,date,freq) values (?,?,?,?);''',
                        [row['user_id'], row['title'], row['next_date'], row['freq']])
                db.commit()
            except IndexError:
                pass
            
        elif len(request.form)==0:
            cur.execute('''UPDATE tasks SET complete=0 where user_id=?;''', [session['user_id']])
            db.commit()
            
        return redirect('/')
            
    elif 'user_id' in session:
        
        rows = [dict(row) for row in cur.execute('''select *, (julianday(date)-julianday('now')+1) as days_to_complete 
                                from tasks
                                where user_id=? and complete=0 
                                order by date asc;''', 
                    [session['user_id']]).fetchall()]
        data = [[row for row in rows if row['days_to_complete']<0],
                [row for row in rows if row['days_to_complete']>=0 and row['days_to_complete']<1],
                [row for row in rows if row['days_to_complete']>=1 and row['days_to_complete']<2],
                [row for row in rows if row['days_to_complete']>=2 and row['days_to_complete']<6],
                [row for row in rows if row['days_to_complete']>=7]]
        
        # removed for now - ability to restore completed tasks
        #finished = [dict(row) for row in cur.execute('''select *
        #                        from tasks 
        #                        where user_id=? and complete=1
        #                        order by date asc;''', 
        #            [session['user_id']]).fetchall()]
        
        return render_template('index.html', data=data)#, finished=finished)
    else:
        return render_template('index.html')
        
@app.route("/edit/<task_id>", methods=['GET', 'POST'])
def edit(task_id):
    '''form to create a new task
    '''
    if request.method == "POST":     
        # update current task with new values
        db = get_db()
        cur = db.cursor()
        
        cur.execute('''UPDATE tasks 
                        set title=?,
                            date=?,
                            freq=?
                        where user_id=? and id=?;''', 
                    [request.form.get("title"), request.form.get("date"), request.form.get("dropdown"), 
                            session['user_id'], task_id])
        db.commit()
        return redirect('/')
    else:
        if 'user_id' in session:
            db = get_db()
            cur = db.cursor()
            
            # make sure current task & user_id are valid
            try:
                row = dict(cur.execute('''select *
                                from tasks
                                where user_id=? and id=?;''', 
                    [session['user_id'], task_id]).fetchall()[0])
            except IndexError:
                return redirect('/')
                #2021-02-22'
            return render_template('edit.html', task_id=task_id, title=row['title'], due_date=row['date'], repeat=row['freq'])
    
@app.route("/new", methods=["GET", "POST"])
def new():
    '''form to create a new task
    '''
    if request.method == "POST":
            
        # add data to database
        db = get_db()
        cur = db.cursor()
                    
        cur.execute('''INSERT INTO tasks (id,title,date,freq) 
           VALUES (?,?,?,?)''', [session['user_id'], request.form.get("title"), request.form.get("date"),
                        request.form.get("dropdown")])
        
        db.commit()
        
        return redirect('/')
        
    else: # get request
        if 'user_id' in session:
            return render_template('new.html')
        else:
            return redirect('/')
    
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

        #try:
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
        
        rows = cur.execute('''select username,id from users where username = ?;''', 
                        [request.form.get("username")]).fetchall()
        # Remember which user has logged in
        session["user_id"] = rows[0][1]
        return redirect('/')

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
            # to-do: actually secure hash
            if row[0]!=hash(request.form.get("password")):
                return redirect('/login')
            else:            
                # Remember which user has logged in
                session["user_id"] = row[1]
                
            # Redirect user to home page
            return redirect('/')
                
        except:
            return redirect('/login')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")