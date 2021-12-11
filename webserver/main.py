from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "0.0.0.0"
serverPort = 8080

# Use placeholders for now, later this can be set through a request
player1 = "Player1"
id1 = "1"
player2 = "Player2"
id2 = "2"

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
        score1 = self.read_file(id1)
        score2 = self.read_file(id2)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<center><h1>Live Dashboard</h1></center>", "utf-8"))
        self.wfile.write(bytes("<div class='row'>", "utf-8"))
        self.wfile.write(bytes("<div class='column' style='text-align: center;'><h2>" + player1 + "</h2><p> " + str(score1) + "</p></div>", "utf-8"))
        self.wfile.write(bytes("<div class='column' style='text-align: center;'><h2>" + player2 + "</h2><p> " + str(score2) + "</p></div>", "utf-8"))
        self.wfile.write(bytes("</div>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        print("Received input: {}".format(body))
        body_as_string = body.decode("utf-8") 

        # There are always 2 oponents in fencing
        # Each will have their point stored in a separate file
        # When each scores, an id will be sent to the scoring server
        # which will then increment the counter for that oponent id
        # The dashboard will be responsible for reading the scores
        # and declaring a winner

        # body comes in format id=<id>
        id = body_as_string.split("=")[1]
        fencer_score_file = 'fencer#' + id + "_score.txt"
        print("Point scored from fencer#" + id)

        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()

        try:
            with open( fencer_score_file , 'r' ) as fle:
                score = int( fle.readline() ) + 1
        except FileNotFoundError:
            score = 1
            print("First point for fencer#" + id)

        with open(  fencer_score_file, 'w' ) as fle:
            fle.write( str(score) )

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), EpeeScoringServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
