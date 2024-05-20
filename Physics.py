import phylib;
import math
import sqlite3;


################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = 2 * BALL_RADIUS
HOLE_RADIUS = 2 * BALL_DIAMETER
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_INTERVAL = 0.01 #changed

#Header & footer
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id= "pool-table" width="700" height="1375" viewBox="-25 -25 1400 2750"xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """<line id="shooting-direction-line" x1="0" y1="0" x2="0" y2="0" stroke="black" stroke-width="0"></line>
</svg>\n </div>\n
  <div>X: <span id="x-coord"></span>, Y: <span id="y-coord"></span></div>\n"""


################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here

    def svg(self):
        """
        Returns an SVG representation of the StillBall.
        """

        return """<circle id="%d" circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.number,
            self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, phylib.PHYLIB_BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]
        )


class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position (x, y), velocity,
        and acceleration as arguments.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_ROLLING_BALL,
                                      number,
                                      pos,
                                      vel,
                                      acc,
                                      0.0,  # Additional parameters for RollingBall
                                      0.0)

        # Convert the phylib_object into a RollingBall class
        self.__class__ = RollingBall

    #SVG :

    def svg(self):
        """
        Returns an SVG representation of the RollingBall.
        """
        return """<circle id="%d" circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.number,
            self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, phylib.PHYLIB_BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number]
        )


class Hole(phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self, pos):
        """
        Constructor function. Requires position (x, y) as an argument.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HOLE,
                                      0,  # Hole doesn't have a number
                                      pos,
                                      None,
                                      None,
                                      0.0,
                                      0.0)

        # Convert the phylib_object into a Hole class
        self.__class__ = Hole

    #SVG:

    def svg(self):
        """
        Returns an SVG representation of the Hole.
        """
        return """<circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (
            self.obj.hole.pos.x, self.obj.hole.pos.y, phylib.PHYLIB_HOLE_RADIUS
        )


class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """
    def __init__(self, y):
        """
        Constructor function. Requires y-coordinate as an argument.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      0,  # HCushion doesn't have a num>
                                      None,
                                      None,
                                      None,
                                      0.0,
                                      y)

        
        # Store the y-coordinate as an attribute
        # Convert the phylib_object into an HCushion class
        self.__class__ = HCushion
    #SVG:
    def svg(self):
        """
        Returns an SVG representation of the HCushion.
        """
        if self.obj.hcushion.y == 0:
            y = -25
        else:
            y = 2700

        return """<rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" %y


class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """
    def __init__(self, x):
        """
        Constructor function. Requires x-coordinate as an argument.
        """
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0,  # VCushion doesn't have a number),  # VCu>
                                      None,
                                      None,
                                      None,
                                      x,
                                      0.0)
        
        # Store the x-coordinate as an attribute
        self.x = x
        # Convert the phylib_object into a VCushion class
        self.__class__ = VCushion
    #SVG:
    def svg(self):
        """
        Returns an SVG representation of the VCushion.
        """
        if self.obj.vcushion.x == 0:
            x = -25
        elif self.obj.vcushion.x == 1350:
            x = 1350
        #x = -25 if self.obj.vcushion.x == 0 elif 1350  # Set x value based on the >
        return """<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" %x



################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg(self):
        """
        Returns SVG representation of the table
        """

        svg_string = HEADER #header

        # Concatenates the SVG representation of each object in the table

        for obj in self:
            if obj is not None:
                svg_string += obj.svg()
        svg_string += FOOTER # add footer

        #retruns string
        return svg_string
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                Coordinate(0,0),
                Coordinate(0,0),
                Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
                # return table
        return new;

    def cueBall(self, xvel, yvel):
        #Method to find ball 0
        #Still & 0
        for ball in self:
            if (isinstance(ball, StillBall) or isinstance(ball, RollingBall)) and ball.obj.still_ball.number == 0:
                return ball   
        return None


class Database():
    
    def __init__(self, reset=False):
        # Set the database file name
        self.db_file = 'phylib.db'

        # If reset is True, delete the existing database file
        if reset:
            self._delete_database()

        # Create/open a database connection and store it as a class attribute
        self.conn = sqlite3.connect(self.db_file)

    def _delete_database(self):
        # Helper method to delete the existing database file
        try:
            # Close the connection before deleting the file
            if hasattr(self, 'conn'):
                self.conn.close()

            # Delete the database file
            if hasattr(self, 'db_file'):
                import os
                os.remove(self.db_file)
        except Exception as e:
            print(f"Error deleting database file: {str(e)}")

    def createDB( self ):
        self.cursor = self.conn.cursor()

        # Create 'Ball' table with necessary parameters (primary key, etc.)
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Ball (
                        BALLID INTEGER PRIMARY KEY AUTOINCREMENT,
                        BALLNO INTEGER NOT NULL,
                        XPOS FLOAT NOT NULL,
                        YPOS FLOAT NOT NULL,
                        XVEL FLOAT,
                        YVEL FLOAT
                    )
                       ''')
        
        # Create 'TTable' table
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS TTable(
                        TABLEID INTEGER PRIMARY KEY AUTOINCREMENT,
                        TIME FLOAT NOT NULL)
                       ''')
        
        # Create 'BallTable' table, referencing Ball and TTable
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS BallTable(
                       BALLID INTEGER NOT NULL,
                       TABLEID INTEGER NOT NULL,
                       FOREIGN KEY(BALLID) REFERENCES Ball(BALLID),
                       FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID))
                       ''')
        
        # Create 'Shot' table with foreign key constraints
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Shot(
                       SHOTID INTEGER PRIMARY KEY AUTOINCREMENT,
                       PLAYERID INTEGER NOT NULL,
                       GAMEID INTEGER NOT NULL,
                       FOREIGN KEY(PLAYERID) REFERENCES Player(PLAYERID),
                       FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID))
                       ''')
        # Create 'Tableshot' table with foreign key constraints
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS TableShot(
                        TABLEID INTEGER NOT NULL,
                        SHOTID INTEGER NOT NULL,
                        FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID)
                        FOREIGN KEY(SHOTID) REFERENCES Shot(SHOTID))
                       ''')
        # Creates 'Game' table 
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Game (
                        GAMEID INTEGER PRIMARY KEY AUTOINCREMENT,
                        GAMENAME VARCHAR(64) NOT NULL)
                        ''')
        # Create 'Player' table 
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Player (
                        PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT,
                        GAMEID INTEGER NOT NULL,
                        PLAYERNAME VARCHAR(64) NOT NULL,
                        FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID))
                        ''')
        
        # Commit the changes and close the cursor
        self.conn.commit()
        self.cursor.close()
        
        
    def readTable(self, tableID):

        self.cursor = self.conn.cursor()

        #Retrieves from TTable, Ball and BallTable tables to get ball attribtes, related via Join
        self.cursor.execute('''
                SELECT TTable.TIME, Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                FROM TTable
                JOIN BallTable ON TTable.TABLEID = BallTable.TABLEID
                JOIN Ball ON BallTable.BALLID = Ball.BALLID
                WHERE TTable.TABLEID = ?
            ''', (tableID + 1,)) #Adjusted tableID to match SQL
        
        #Commit changes
        self.conn.commit()

        # Fetch all the rows as a list of tuples
        result = self.cursor.fetchall()


        #Checks if empty
        if not result: 
            return None

        #Take time from 1st row
        time = result[0][0]


        #Make table object
        table = Table()
        table.time = time

        # Iterate over the rows and create Ball objects
        for row in result:
            ball_id, ball_no, x_pos, y_pos, x_vel, y_vel = row[1:]

            if x_vel is not None and y_vel is not None:
                speed = math.sqrt(x_vel ** 2 + y_vel ** 2)
            else:
                # Set x_vel and y_vel to 0 if either is None
                x_vel = x_vel if x_vel is not None else 0
                y_vel = y_vel if y_vel is not None else 0
                speed = math.sqrt(x_vel ** 2 + y_vel ** 2)

            # Check if the ball has no velocity
            if speed > VEL_EPSILON:

                x_acc = -x_vel / speed * DRAG
                y_acc = -y_vel / speed * DRAG

                ball = RollingBall(ball_no, Coordinate(x_pos, y_pos), Coordinate(x_vel, y_vel), Coordinate(x_acc, y_acc))
                #print("RB  in read;")
            else:
                # Calculate the acceleration for RollingBalls
                ball = StillBall(ball_no, Coordinate(x_pos, y_pos))

            # Add the ball to the table
            table += ball

        # Close the cursor and return the Table object
        self.cursor.close()
        self.conn.commit()
        return table

    def writeTable( self, table ):
        self.cursor = self.conn.cursor()
        
        # Insert a new entry into TTable to get a new TABLEID
        self.cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        self.conn.commit()

        #Get autoincremented TABLEID
        tableID = self.cursor.lastrowid

        #Iterate over balls in table & insert into Ball & BallTable tables
        for ball in table:
            if ball is not None and ball.type is not None:
                if ball.type == phylib.PHYLIB_STILL_BALL:
                    self.cursor.execute('''
                        INSERT INTO BALL(BALLNO, XPOS, YPOS, XVEL, YVEL)
                        VALUES(?,?,?,?,?)
                        ''', (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y, None, None))
                    self.conn.commit()

                    #Get BALLID
                    ballID = self.cursor.lastrowid

                    #Put into ballTable
                    self.cursor.execute('''
                        INSERT INTO BallTable(BALLID, TABLEID)
                        VALUES (?, ?)
                        ''', (ballID, tableID))
                    self.conn.commit()

                elif ball.type == phylib.PHYLIB_ROLLING_BALL:
                    self.cursor.execute('''
                        INSERT INTO BALL(BALLNO, XPOS, YPOS, XVEL, YVEL)
                        VALUES(?,?,?,?,?)
                        ''', (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
                    self.conn.commit()
                    #Get BALLID
                    ballID = self.cursor.lastrowid

                    #Put into ballTable
                    self.cursor.execute('''
                        INSERT INTO BallTable(BALLID, TABLEID)
                        VALUES (?, ?)
                        ''', (ballID, tableID))
                    self.conn.commit()

        #Close
        self.cursor.close()
        self.conn.commit()

        return tableID -1
        
    def close(self):
        # Commit changes and close the connection
        self.conn.commit()
        self.conn.close()

    def getGame (self, gameID):
        self.cursor = self.conn.cursor()

        #Query to retrieve game info based on gameID
        self.cursor.execute('''
            SELECT G.GAMEID, G.GAMENAME, MIN(P1.PLAYERNAME) AS player1Name, MAX(P2.PLAYERNAME) AS player2Name
            FROM Game G
            JOIN Player P1 ON G.GAMEID = P1.GAMEID
            JOIN Player P2 ON G.GAMEID = P2.GAMEID
            WHERE G.GAMEID = ?;
        ''', (gameID + 1,))

        #Fetch query result
        result = self.cursor.fetchone()

        #Commit & close
        self.conn.commit()
        self.cursor.close()

        return result
    
    def setGame(self, gameName, player1Name, player2Name):
        self.cursor = self.conn.cursor()

        # Insert a new game into the Game table
        self.cursor.execute ('''
            INSERT INTO Game (GAMENAME) 
            VALUES (?)
            ''', (gameName,))
        gameID = self.cursor.lastrowid

        # Insert a new player (player1) into the Player table
        self.cursor.execute('''
        INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?,?);
        ''', (gameID, player1Name))

        #Retrieve ID
        player1ID = self.cursor.lastrowid

        # Insert a new player (player2) into the Player table
        self.cursor.execute('''
        INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?,?);
        ''', (gameID, player2Name))

        #Retrieve ID
        player2ID = self.cursor.lastrowid
        
        self.conn.commit()
        self.cursor.close()

        #Return ID -1 to match what's required by SQL
        return gameID - 1 
    

    def newShot(self, gameName, playerName):

        self.cursor = self.conn.cursor()
    
        # Look up the playerID based on the playerName
        playerID = self.lookupPlayerID(playerName)

        # Look up the gameID based on the gameName
        gameID = self.lookupGameID(gameName)

        if playerID is None or gameID is None:
            return None

        # Insert a new shot into the Shot table
        self.cursor.execute('''
            INSERT INTO Shot (PLAYERID, GAMEID)
            VALUES (?, ?)
        ''', (playerID, gameID))

        self.conn.commit()

        # Get the last inserted row ID (shotID)
        shotID = self.cursor.lastrowid

        # Commit the transaction
        self.conn.commit()

        return shotID
    
    #Helper for newShot
    def lookupPlayerID(self, playerName):
        # Query the Player table to find the player ID based on playerName
        self.cursor.execute('''
            SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?
        ''', (playerName,))

        # Fetch the result (assuming there's only one matching player)
        result = self.cursor.fetchone()

        #Return if exists
        if result:
            playerID = result[0]
            return playerID
        else:
            # Player not found
            return None
        
    #Helper for newShot
    def lookupGameID(self, gameName):
        # Query the Game table to find the game ID based on gameName
        self.cursor.execute('''
            SELECT GAMEID FROM Game WHERE GAMENAME = ?
        ''', (gameName,))

        # Fetch the result (assuming there's only one matching game)
        result = self.cursor.fetchone()

        #Return if exissts
        if result:
            gameID = result[0]
            return gameID
        else:
            # Game not found
            return None
        
    def getTableIDByTime(self, time):

        # Execute the SQL SELECT statement
        self.cursor.execute('''
            SELECT TABLEID FROM TTable WHERE abs(TIME - ?) < 0.001
        ''', (time,))

        # Fetch the result
        result = self.cursor.fetchone()

        # Check if result is not empty
        if result:
            tableId = result[0]  # Return the TABLEID
            return tableId
        else:
            return None  # Return None if no matching record found

        

class Game ():

    def __init__( self, gameID=None, gameName=None, player1Name=None,
player2Name=None ):
        if gameID is not None and (gameName is not None or player1Name is not None or player2Name is not None):
            raise TypeError("Invalid combination of arguments")
        
        self.gameID = None #Set after insert
        self.gameName = None
        self.player1Name = None
        self.player2Name = None
        
        #Create database, make sure tables exist
        self.db = Database()
        self.db.createDB()
        self.tableDict = {}

        if gameID is not None:
            #1st consrtuctor
            result = self.db.getGame(gameID)
            if result:
                self.gameID, self.gameName, self.player1Name, self.player2Name = result
            else:
                raise ValueError(f"No game found with gameID {gameID}.")
        elif gameName is not None and player1Name is not None and player2Name is not None:
            #2nd constructor
            self.gameID = self.db.setGame(gameName, player1Name, player2Name)
            self.gameName = gameName

            #Set Player1 to be the lower
            self.player1Name = player1Name
            self.player2Name = player2Name

        else:
            raise TypeError("Invalid combination of arguments for constructor.")
        
    def shoot( self, gameName, playerName, table, xvel, yvel ):

        
        self.cursor = self.db.conn.cursor()

        #New shot added 
        newShotID = self.db.newShot(gameName, playerName)

        #Cue ball located
        cue_ball = table.cueBall(xvel, yvel)
        

        #Cue ball's parameters set
        if cue_ball.type == phylib.PHYLIB_STILL_BALL:
            xpos = cue_ball.obj.still_ball.pos.x
            ypos = cue_ball.obj.still_ball.pos.y
        elif cue_ball.type == phylib.PHYLIB_ROLLING_BALL:
            xpos = cue_ball.obj.rolling_ball.pos.x
            ypos = cue_ball.obj.rolling_ball.pos.y


        # Check if either xvel or yvel is None and assign 0 to the missing value
        xvel = xvel if xvel is not None else 0
        yvel = yvel if yvel is not None else 0


        if xvel is not None and yvel is not None:
                speed = math.sqrt(xvel ** 2 + yvel ** 2)
        else:
            speed = 0

        # Check if the ball has no velocity, set acceleration as in A2
        if speed > VEL_EPSILON:
            xacc = -xvel / speed * DRAG
            yacc = -yvel / speed * DRAG
        else:
            xacc = 0
            yacc = 0

        #Set it to rolling & number to 0
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL
        cue_ball.obj.rolling_ball.number = 0

        #Set all parameters for cue ball as a rolling ball
        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel
        cue_ball.obj.rolling_ball.acc.x = xacc
        cue_ball.obj.rolling_ball.acc.y = yacc

        # Save the original table to the database
        table_id = self.db.writeTable(table)
        
        # Record the table in TableShot
        self.cursor.execute('''
            INSERT INTO TableShot (TABLEID, SHOTID)
            VALUES (?, ?)
        ''', (table_id, newShotID))
        self.db.conn.commit()

        svg_content = ""

        #Loop calling segment repeatedly
        while True:
            
            start_time = table.time

            segment = table.segment()

            #Break when none is returned
            if segment is None:
                break
            
            #Length of seg in seconds (end - beginning)
            seg_len = segment.time - table.time

            #Frames in segment
            num_frames = math.floor(seg_len/FRAME_INTERVAL)

            # Loop over the time intervals
            for frame_index in range(num_frames):

                #Calculate time for next frame
                next_frame_time = (frame_index) * FRAME_INTERVAL

                #Simulate next frame by rolling
                new_table = table.roll(next_frame_time)

                # Set the time of the returned table
                new_table.time = table.time + next_frame_time

                # Save the table to the database
                table_id = self.db.writeTable(new_table)

                svg_content += new_table.svg()
                self.tableDict[table_id] = new_table
                
                # Record the table in TableShot
                self.cursor.execute('''
                    INSERT INTO TableShot (TABLEID, SHOTID)
                    VALUES (?, ?)
                ''', (table_id, newShotID))
            
            table = segment

            self.db.conn.commit()
            #cursor.close()

        self.cursor.close()
        return self.tableDict, svg_content
        #return svg_content
    
    