select user_id, response 
from responses 
where question_id = 1 
and user_id in 
('0bbc8eef32dadbbf7a4cb500c36c2cd0',
'13143c6e2a314bdeffe7d20732e3f262',
'4504663a8fd24410162375ab37e25c1c',
'99447d7f6672efac075b01d157737580',
'a8d5c7b8fa369036b7e37ffa07fe2351'
)
INTO OUTFILE '/var/lib/mysql-files/q1.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select user_id, response 
from responses 
where question_id = 2 
and user_id in 
('0bbc8eef32dadbbf7a4cb500c36c2cd0',
'13143c6e2a314bdeffe7d20732e3f262',
'4504663a8fd24410162375ab37e25c1c',
'99447d7f6672efac075b01d157737580',
'a8d5c7b8fa369036b7e37ffa07fe2351'
)
INTO OUTFILE '/var/lib/mysql-files/q2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';


select user_id, response 
from responses 
where question_id = 3 
and user_id in 
('0bbc8eef32dadbbf7a4cb500c36c2cd0',
'13143c6e2a314bdeffe7d20732e3f262',
'4504663a8fd24410162375ab37e25c1c',
'99447d7f6672efac075b01d157737580',
'a8d5c7b8fa369036b7e37ffa07fe2351'
)
INTO OUTFILE '/var/lib/mysql-files/q3.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select user_id, response 
from responses 
where question_id = 4
and user_id in 
('0bbc8eef32dadbbf7a4cb500c36c2cd0',
'13143c6e2a314bdeffe7d20732e3f262',
'4504663a8fd24410162375ab37e25c1c',
'99447d7f6672efac075b01d157737580',
'a8d5c7b8fa369036b7e37ffa07fe2351'
)
INTO OUTFILE '/var/lib/mysql-files/q4.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select user_id, response 
from responses 
where question_id = 5
and user_id in 
('0bbc8eef32dadbbf7a4cb500c36c2cd0',
'13143c6e2a314bdeffe7d20732e3f262',
'4504663a8fd24410162375ab37e25c1c',
'99447d7f6672efac075b01d157737580',
'a8d5c7b8fa369036b7e37ffa07fe2351'
)
INTO OUTFILE '/var/lib/mysql-files/q5.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select user_id, response 
from responses 
where question_id = 6
and user_id in 
('0bbc8eef32dadbbf7a4cb500c36c2cd0',
'13143c6e2a314bdeffe7d20732e3f262',
'4504663a8fd24410162375ab37e25c1c',
'99447d7f6672efac075b01d157737580',
'a8d5c7b8fa369036b7e37ffa07fe2351'
)
INTO OUTFILE '/var/lib/mysql-files/q6.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select user_id, response 
from responses 
where question_id = 6
and user_id in 
('0bbc8eef32dadbbf7a4cb500c36c2cd0',
'13143c6e2a314bdeffe7d20732e3f262',
'4504663a8fd24410162375ab37e25c1c',
'99447d7f6672efac075b01d157737580',
'a8d5c7b8fa369036b7e37ffa07fe2351'
)
INTO OUTFILE '/var/lib/mysql-files/q7.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

