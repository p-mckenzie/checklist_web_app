DELETE FROM users WHERE username='test';
DELETE FROM tasks WHERE user_id=1;	
INSERT INTO users (username,hash,id) values ('test',116,1);
INSERT INTO tasks (user_id,title,date,freq) values 
		(1,'Laundry',date('now','-1 days'),1),
		(1,'Run dishwasher',date('now'),0),
		(1,'Take cat to vet',date('now','+1 days'),2),
		(1,'Take out the trash',date('now','+2 days'),3),
		(1,'Get haircut',date('now','+3 days'),4),
		(1,'Grocery shop',date('now','+4 days'),1),
		(1,'Clean bathroom',date('now','+5 days'),1),
		(1,'Organize bookshelf',date('now','+12 days'),1);