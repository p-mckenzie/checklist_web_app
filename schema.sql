CREATE TABLE IF NOT EXISTS 'users' 
        ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        'username' TEXT NOT NULL, 
        'hash' INT NOT NULL);
CREATE TABLE IF NOT EXISTS 'tasks'
    ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	'user_id' TEXT NOT NULL,
    'title' TEXT NOT NULL,
    'date' TEXT NOT NULL,
    'freq' INT NOT NULL DEFAULT 1,
    'complete' INT NOT NULL DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id));
	
INSERT INTO users (username,hash) values ('test',116);
INSERT INTO tasks (user_id,title,date,freq) values 
		(1,'Neg',date('now','-1 days'),1),
		(1,'Foo',date('now','+1 days'),1),
		(1,'Bar',date('now','+2 days'),1),
		(1,'Baz',date('now','+3 days'),1),
		(1,'Qux',date('now','+4 days'),1),
		(1,'Quux',date('now','+5 days'),1);