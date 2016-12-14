#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    query = "DELETE FROM Records"
    c.execute(query)
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    query = "DELETE FROM Players"
    c.execute(query)
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    query = "SELECT COUNT(*) FROM Players P"
    c.execute(query)
    num = c.fetchone()[0]
    print num
    DB.close()
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    query = "INSERT INTO Players (name) VALUES (%s)"
    name = bleach.clean(name) # in case bad input
    c.execute(query, (name,))
    DB.commit()
    DB.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    """
    SELECT P.id, P.name, count(R.winner) as wins, temp.matches 
    FROM Players P LEFT JOIN Records R ON P.id = R.winner, 
         (SELECT P2.id, count(P2.id) as matches 
          FROM Players P2, Records R2 WHERE P2.id = R2.id1 OR P2.id = R2.id2 GROUP BY P2.id) as temp
    WHERE P.id = temp.id 
    GROUP BY P.id, temp.matches 
    ORDER BY wins desc;
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    query = """ 
    SELECT P.id, P.name, count(R.winner) as wins, temp.matches 
    FROM Players P LEFT JOIN Records R ON P.id = R.winner, 
         (SELECT P2.id, count(R2.id1 + R2.id2) as matches 
          FROM Players P2 LEFT JOIN Records R2 ON P2.id = R2.id1 OR P2.id = R2.id2 GROUP BY P2.id) as temp
    WHERE P.id = temp.id 
    GROUP BY P.id, temp.matches 
    ORDER BY wins desc
    """
    c.execute(query)
    standings = c.fetchall()
    DB.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    query = "INSERT INTO Records values (%s, %s, %s, %s)"
    # Parameters are int, don't need to bleach
    c.execute(query,(winner,loser,winner,loser,))
    DB.commit()
    DB.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()

    # Use player standings table (ordered starting by most wins)
    # Format: [(id, name, wins, matches), ...]
    pairingList = playerStandings()
    print pairingList[0][0]
    # Pair up first with second, third with fourth, etc... 
    # Using simple loop.. ie
    # while i != length of list
    # store row[i] in x, ++i, store row[i] in y, pair up x and y and repeat

    i = 0
    swissResults = []
    while (i != len(pairingList)):
        id1 = pairingList[i][0]
        name1 = pairingList[i][1]
        i = i + 1
        id2 = pairingList[i][0]
        name2 = pairingList[i][1]
        i = i + 1
        print i
        swissResults.append((id1, name1, id2, name2))

    return swissResults

