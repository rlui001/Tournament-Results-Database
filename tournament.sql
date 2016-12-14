-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
CREATE TABLE Players (	id serial,
						name text,
						primary key(id));

CREATE TABLE Records (	id1 integer,
						id2 integer,
						winner integer,
						loser integer,
						primary key(id1, id2),
						foreign key (id1) references Players(id),
						foreign key (id2) references Players(id));

--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


