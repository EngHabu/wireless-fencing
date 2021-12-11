from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "0.0.0.0"
serverPort = 8080

class EpeeScoringServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

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
