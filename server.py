import http.server
import sqlite3;
import json
import sys #to get argv
import urllib
import os
import cgi; # used to parse Mutlipart FormData 
import math
import Physics
import random
import time
import re

# web server
from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import urlparse, parse_qs

from urllib.parse import urlparse, parse_qsl

def make_table():

        # Construct a Table and add Balls
            table = Physics.Table()
            #Physics.Table.__init__(table)

            # Create Still Balls

            pos1 = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_WIDTH / 2.0)
            sb1 = Physics.StillBall(1, pos1)
            table += sb1

            pos2 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER + 4.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0) 
            )
            sb2 = Physics.StillBall(2, pos2)
            table += sb2

            pos3 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER + 4.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0) 
            )
            sb3 = Physics.StillBall(3, pos3)
            table += sb3

            pos4 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 - ((Physics.BALL_DIAMETER * 2) + 8.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * ((Physics.BALL_DIAMETER * 2)+ 6.0) 
            )
            sb4 = Physics.StillBall(4, pos4)
            table += sb4

            pos5 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 + ((Physics.BALL_DIAMETER * 2) + 8.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * ((Physics.BALL_DIAMETER * 2)+ 6.0) 
            )
            sb5 = Physics.StillBall(5, pos5)
            table += sb5

            pos6 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * ((Physics.BALL_DIAMETER * 2)+ 6.0) 
            )
            sb6 = Physics.StillBall(8, pos6)
            table += sb6

            pos7 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER + 4.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 3 + 6.0) 
            )
            sb7 = Physics.StillBall(6, pos7)
            table += sb7

            pos8 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER + 4.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 3 + 6.0) 
            )
            sb8 = Physics.StillBall(7, pos8)
            table += sb8

            pos9 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER * 3 + 4.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 3 + 10.0) 
            )
            sb9 = Physics.StillBall(9, pos9)
            table += sb9

            pos10 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER * 3 + 4.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 3 + 10.0) 
            )
            sb10 = Physics.StillBall(10, pos10)
            table += sb10

            pos11 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * ((Physics.BALL_DIAMETER * 4)+ 6.0) 
            )
            sb11 = Physics.StillBall(11, pos11)
            table += sb11

            pos12 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER * 2 + 8.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 4 + 10.0) 
            )
            sb12 = Physics.StillBall(12, pos12)
            table += sb12

            pos13 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER * 2 + 8.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 4 + 10.0) 
            )
            sb13 = Physics.StillBall(13, pos13)
            table += sb13

            pos14 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER * 4 + 8.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 4 + 10.0) 
            )
            sb14 = Physics.StillBall(14, pos14)
            table += sb14

            pos15 = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER * 4 + 8.0) / 2.0 ,
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 4 + 10.0) 
            )
            sb15 = Physics.StillBall(15, pos15)
            table += sb15

            pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + random.uniform( -3.0, 3.0 ),
                          Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
            sb  = Physics.StillBall( 0, pos );

            table += sb;

            return table

# handler for our web-server - for GET and POST requests
class MyHandler(BaseHTTPRequestHandler):

    db = Physics.Database( reset=True );
    db.createDB();
    table = make_table()  # Initialize table once
    svg_contents = []
    retrievedTables = {}

    def do_GET(self):
         # parse URL to get the path and form data
        parsed = urlparse(self.path)

        # check if the web-pages matches handled options
        if self.path.endswith(".html"):

            # Get the HTML file
            fp = open('.'+self.path)
            content = fp.read()

            #Generate headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #send to browser
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        #check web page for table svg's
        #elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
        #    self.serve_svg_file(parsed.path)

        elif self.path.endswith(".js"):
            # Serve JavaScript file
            fp = open('.' + self.path)
            content = fp.read()
            fp.close()

            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')  # Set content type to JavaScript
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))

        elif parsed.path == '/get_updated_svg':

            # Retrieve the updated SVG contents from the database or wherever it's stored
            updated_svg = self.svg_contents  

            # Send the SVG contents as the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'svg_contents': updated_svg}).encode('utf-8'))

        #else generate error 
        else:
            print(parsed.path)
            print('404 end of GET')
            self.send_404_error()

    def do_POST(self):
        global current_game_id
        global p1N
        global p2N

        parsed = urlparse(self.path)

        if parsed.path in ['/pool.html']:
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            required_fields = ['player1Name', 'player2Name', 'gameName']
            for field in required_fields:
                if field not in form_data:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Error: player name missing.")
                    return
                
            p1N = form_data['player1Name'].value
            p2N = form_data['player2Name'].value
            game_name = form_data['gameName'].value

            game = Physics.Game(gameName=game_name, player1Name=p1N, player2Name=p2N)
            current_game_id = game.gameID

            index = 0
            svg_files = []

            while self.table:
                svg_content = self.table.svg()
                file_name = f"table_{index}.svg"
                with open(file_name, "w") as file:
                    file.write(svg_content)
                svg_files.append(file_name)
                index += 1
                self.table = self.table.segment()

            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pool Game</title>
    <style>
                /* CSS */
                #pool-table-container {{
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    text-align: center;
                    }}

                #game-info {{
                    position: fixed;
                    top: 50%;
                    left: 10%; /* Adjust the left position as needed */
                    transform: translateY(-50%);
                    background-color: rgba(255, 255, 255, 0.8);
                    padding: 20px; /* Adjust padding as needed */
                    border-radius: 10px;
                    border: 2px solid #333;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                }}

                #game-info div {{
                    margin-bottom: 10px; /* Adjust margin as needed */
                }}

                #game-info span {{
                    font-size: 18px; /* Adjust font size based on viewport width */
                    font-weight: bold;
                    color: #333;
                }}

            </style>
</head>
<body>
    <div id="pool-table-container">
        {svg_content}
            <div id="game-info">
            <div>Game Name: <span id="game-name">{game_name}</span></div>
            <div>Player 1: <span id="player1-name">{p1N}</span></div>
            <div>Player 2: <span id="player2-name">{p2N}</span></div>
        </div>
        <script>
        document.addEventListener("DOMContentLoaded", function() {{
            var currentPlayerIndex = 0;
            var players = [{p1N}, {p2N}]; // Names of players
            var playerTurnElement = document.getElementById("player-turn");

            // Function to switch the player's turn
            function switchPlayerTurn() {{
                currentPlayerIndex = (currentPlayerIndex + 1) % players.length;
                playerTurnElement.innerText = "Player's Turn: " + players[currentPlayerIndex];
            }}

            // Initial display of player's turn
            switchPlayerTurn();

        }});
    </script>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
<script src="track.js"></script>
</body>
</html>
""".replace("{svg_content}", svg_content).replace("{p1N}", p1N).replace("{p2N}", p2N).replace("{game_name}", game_name)
            with open('pool.html', 'w') as html_file:
                html_file.write(html_content)

            self.send_response(302)
            self.send_header('Location', '/pool.html')
            self.end_headers()


        elif parsed.path == '/trigger_shoot':

            # Parse the incoming JSON data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract velocity data
            xVel = data['velocityX']
            yVel = data['velocityY']

            print(xVel)
            print(yVel)

            # Retrieve the current game using the stored game ID
            game = Physics.Game(gameID=current_game_id)

            if game is None:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Game not found.")
                return

            # Perform shoot action
            retrievedTables, updated_svg = game.shoot(game.gameName, game.player1Name, self.table, xVel, yVel)


            pattern = r'<svg.*?</svg>'
            input_svg = updated_svg
            matches = re.findall(pattern, input_svg, re.DOTALL)
            
            for table_id, match in enumerate(matches, start=1):

            # Wrap SVG content within a <g> group with a unique ID
                svg_with_group = f'<g id="svg_img_{table_id}">{match}</g>'
                self.svg_contents.append(svg_with_group)

                # Update the database with the new table
                if table_id in retrievedTables:  # Check if the key exists in retrievedTables
                    self.db.writeTable(retrievedTables[table_id])

                    for i in range(10, 26):
                        item = retrievedTables[table_id].__getitem__(i)
                        if isinstance( item, Physics.RollingBall ) or isinstance ( item, Physics.StillBall ):
                            for obj in retrievedTables[table_id] :
                                if isinstance (obj, Physics.Hole):
                                    dist = math.sqrt((item.obj.rolling_ball.pos.x - obj.obj.hole.pos.x) ** 2 + (item.obj.rolling_ball.pos.y- obj.obj.hole.pos.y) ** 2) - Physics.HOLE_RADIUS
                                    # Check if the cue ball has gone into the hole
                                    if dist < Physics.HOLE_RADIUS:
                                        if i == 25:
                                            self.sinkBall(0, table_id)
                                            print("sunk ball 0 ")
                                        else:
                                            self.sinkBall(i - 9, table_id)
                                            print("sunk ball", i - 9)
                                            
                else:
                    print(f"Table with ID {table_id} not found in retrievedTables")

            # Send the updated HTML content back to the client

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

        else:
            # Invalid path
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error: Page not found.")
    
    def sinkBall(self, ball_index, table_id):
        # Iterate through the SVG contents and remove the SVG element corresponding to the ball index
        svg_content = self.svg_contents[table_id - 1]
        pattern = r'<circle\s+id="{}"\s+.*?</circle>'.format(ball_index)
        updated_svg_content = re.sub(pattern, '', svg_content)
        self.svg_contents[table_id - 1] = updated_svg_content

    #helper method for acceleration
    def compute_acceleration(self, velX, velY):

        #calculated similarly to bounce
        speed = math.sqrt(velX ** 2 + velY ** 2)

        if speed > Physics.VEL_EPSILON:
            acc_x = -velX / speed * Physics.DRAG
            acc_y = -velX / speed * Physics.DRAG
        else:
            acc_x = 0.0
            acc_y = 0.0

        return Physics.Coordinate(acc_x, acc_y)

    #helper method to serve svg files
    def serve_svg_file(self, path):

        #constructs the full path to the requested file
        filename = '.' + path
        if os.path.exists(filename): #Checks if the file exists in the specified path
            with open(filename, 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                #self.wfile.write(content)
        else:
            print('404 send SVG')
            self.send_404_error()

    #helper method to delete files
    def delete_svg_files(self):

        # Delete all table-?.svg files in the server's directory
        for filename in os.listdir('.'):
            if filename.startswith('table-') and filename.endswith('.svg'):
                os.remove(filename)

    #helper method to send 404 error
    def send_404_error(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'File Not Found')

    def send_svg_to_server(self, content):
        port = int(sys.argv[1])
        connection = http.client.HTTPConnection('your_server_address', port)
        headers = {'Content-type': 'image/svg+xml'}
        connection.request('POST', '/endpoint_for_svg_files', content, headers)
        response = connection.getresponse()
        return response.read().decode('utf-8')


if __name__ == '__main__':

    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    #Take command line arg as port
    port = 58267

    server_address = ('localhost', port)

    print("serving on : ", server_address)

    # Create an instance of HTTPServer with the server address and MyHandler class
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever() #Serve indefinitely
    
