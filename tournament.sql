-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.


CREATE TABLE Players (	id serial,
						name text,
						primary key(id));

CREATE TABLE Match (	m_id serial,
						winner integer,
						loser integer,
						primary key(m_id),
						foreign key (winner) references Players(id),
						foreign key (loser) references Players(id));

CREATE VIEW Num_Matches AS 
SELECT P2.id, count(M.m_id) as matches 
FROM Players P2 
LEFT JOIN Match M ON P2.id = M.winner OR P2.id = M.loser 
GROUP BY P2.id;	

--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


