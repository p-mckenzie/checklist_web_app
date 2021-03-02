CREATE TABLE IF NOT EXISTS 'users' 
        ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        'username' TEXT NOT NULL, 
        'hash' TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS 'tasks'
    ('username' TEXT NOT NULL,
    'title' TEXT NOT NULL,
    'desc' TEXT NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username));