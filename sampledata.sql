DELETE FROM users WHERE username='test';
DELETE FROM tasks WHERE user_id=1;	
INSERT INTO users (username,hash,id) values ('test',116,1);
INSERT INTO tasks (user_id,title,date,freq) values 
		(1,'Neg',date('now','-1 days'),1),
		(1,'Now',date('now'),0),
		(1,'Foo',date('now','+1 days'),2),
		(1,'Bar',date('now','+2 days'),3),
		(1,'Baz',date('now','+3 days'),4),
		(1,'Qux',date('now','+4 days'),1),
		(1,'Quux',date('now','+5 days'),1),
		(1,'Later',date('now','+12 days'),1);