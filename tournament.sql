-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
CREATE VIEW Num_Matches AS 
SELECT P2.id, count(R2.m_id) as matches 
FROM Players P2 
LEFT JOIN Records R2 ON P2.id = R2.winner OR P2.id = R2.loser 
GROUP BY P2.id;	


CREATE TABLE Players (	id serial,
						name text,
						primary key(id));

CREATE TABLE Records (	m_id serial,
						winner integer,
						loser integer,
						primary key(m_id),
						foreign key (winner) references Players(id),
						foreign key (loser) references Players(id));

--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


