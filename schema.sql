CREATE TABLE IF NOT EXISTS 'users' 
        ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        'username' TEXT NOT NULL, 
        'hash' INT NOT NULL);
CREATE TABLE IF NOT EXISTS 'tasks'
    ('id' TEXT NOT NULL,
    'title' TEXT NOT NULL,
    'date' TEXT NOT NULL,
    'freq' INT NOT NULL,
    FOREIGN KEY(id) REFERENCES users(id));
	
INSERT INTO users (username,hash) values ('test',116);
INSERT INTO tasks (id,title,date,freq) values 
		(1,'Foo',date('now','+1 days'),1),
		(1,'Bar',date('now','+2 days'),1),
		(1,'Baz',date('now','+3 days'),1);