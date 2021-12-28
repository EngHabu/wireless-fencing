from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime

hostName = "0.0.0.0"
serverPort = 8080

# Use placeholders for now, later this can be set through a request
player1 = "Player1"
id1 = "1"
player2 = "Player2"
id2 = "2"

# To prevent multi point counts
DOUBLE_TOUCH_THRESHOLD_MILLISECONDS = 40
MIN_TIME_BETWEEN_TOUCHES_MILLISECONDS = 1000  # set as an upper limit to fencer recording another point

last_touch_time = datetime.datetime.now()
last_touch_fencer_id = ""

class EpeeScoringServer(BaseHTTPRequestHandler):

    def read_file(self, id):
        fencer_score_file = 'fencer#' + id + "_score.txt"
        try:
            with open( fencer_score_file , 'r' ) as fle:
                score = int( fle.readline() )
        except FileNotFoundError:
            score = 0
        return score

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        score1 = self.read_file(id1)
        score2 = self.read_file(id2)
        
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<center><h1>Live Dashboard</h1></center>", "utf-8"))
        self.wfile.write(bytes("<div class='row'>", "utf-8"))
        self.wfile.write(bytes("<div class='column' style='text-align: center;'><h2>" + player1 + "</h2><p> " + str(score1) + "</p></div>", "utf-8"))
        self.wfile.write(bytes("<div class='column' style='text-align: center;'><h2>" + player2 + "</h2><p> " + str(score2) + "</p></div>", "utf-8"))
        self.wfile.write(bytes("</div>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    
    def is_touch_invalid(self, fencer_id):
        global last_touch_fencer_id
        global last_touch_time
        current_time = datetime.datetime.now()
        time_delta_in_milliseconds = (current_time - last_touch_time).total_seconds() * 1000

        # Do not record a point if the touch came from same fencer within a
        # second, or from another fencer within
        # DOUBLE_TOUCH_THRESHOLD_MILLISECONDS (review fencing rules)
        ignore_point = False

        if DOUBLE_TOUCH_THRESHOLD_MILLISECONDS <= time_delta_in_milliseconds <= MIN_TIME_BETWEEN_TOUCHES_MILLISECONDS and last_touch_fencer_id != fencer_id:
            print("Other fencer touch, but too late!")
            ignore_point = True
        if time_delta_in_milliseconds < MIN_TIME_BETWEEN_TOUCHES_MILLISECONDS and last_touch_fencer_id == fencer_id:
            print("Same fencer touch, ignore touch!")
            ignore_point = True
        
        if not ignore_point:    
            last_touch_fencer_id = id
            last_touch_time = current_time

        return ignore_point

    def score_point(self, fencer_id):
        fencer_score_file = 'fencer#' + fencer_id + "_score.txt"
        try:
            with open( fencer_score_file , 'r' ) as fle:
                score = int( fle.readline() ) + 1
                print("Point scored for fencer#" + fencer_id)
        except FileNotFoundError:
            score = 1
            print("First point for fencer#" + fencer_id)

        with open(  fencer_score_file, 'w' ) as fle:
            fle.write( str(score) )

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        print("Received input: {}".format(body))
        body_as_string = body.decode("utf-8") 

        # There are always 2 oponents in fencing. Each will have their point
        # stored in a separate file. When each scores, an id will be sent to the
        # scoring server which will then increment the counter for that oponent
        # id The dashboard will be responsible for reading the scores and
        # declaring a winner.

        # body comes in format id=<id>
        id = body_as_string.split("=")[1]
        print("Touch from fencer#" + id)

        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()

        if self.is_touch_invalid(id):
            print("Touch ignored!")
            return

        self.score_point(id)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), EpeeScoringServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
