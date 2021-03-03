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