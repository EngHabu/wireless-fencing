from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import os
import threading
import time
import asyncio
from fastapi.staticfiles import StaticFiles

class Event_ts(asyncio.Event):
    #TODO: clear() method
    def set(self):
        #FIXME: The _loop attribute is not documented as public api!
        self._loop.call_soon_threadsafe(super().set)

app = FastAPI()
app.mount("/static", StaticFiles(directory="webserver/static"), name="static")

hostName = "0.0.0.0"
serverPort = 8080

# Use placeholders for now, later this can be set through a request
fencer1 = "fencer1"
fencer1_id = "1"
fencer2 = "fencer2"
fencer2_id = "2"

# To prevent multi point counts
DOUBLE_TOUCH_THRESHOLD_MILLISECONDS = 40
MIN_TIME_BETWEEN_TOUCHES_MILLISECONDS = 1000  # set as an upper limit to fencer recording another point

last_touch_time = datetime.datetime.now()
last_touch_fencer_id = ""

point_scored = Event_ts()

@app.get("/")
async def get():
    return HTMLResponse(get_html("webserver/pages/scoreboard.html"))

@app.get("/fencers")
async def get():
    return HTMLResponse(get_html("webserver/pages/fencers.html"))

@app.get("/newbout")
async def get(fencer1_name: str, fencer2_name: str):
    global fencer1, fencer2

    # capture new names and reset scores
    fencer1 = fencer1_name
    fencer2 = fencer2_name
    reset_score(fencer1_id)
    reset_score(fencer2_id)

    return "New game started!"

@app.get("/touch")
async def get(id: str):
    # There are always 2 oponents in fencing. Each will have their point
    # stored in a separate file. When each scores, an id will be sent to the
    # scoring server which will then increment the counter for that oponent
    # id The scoreboard will be responsible for reading the scores and
    # declaring a winner.
    print("Touch from fencer#" + id)

    if is_touch_invalid(id):
        print("Touch ignored!")
        return

    score_point(id)
    point_scored.set()

    return get_score(id)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # TODO: make that event based
        print("waiting...")
        await point_scored.wait()
        point_scored.clear()
        # time.sleep(1)

        print('refreshing scoreboard..')
        updated_score = fencer1 + "," + str(get_score(fencer1_id)) + "," + fencer2 + "," + str(get_score(fencer2_id))
        await websocket.send_text(updated_score)

def get_html(path): 
    html_page = ""
    try:
        with open(path, 'r') as fle:
            html_page = fle.read()
    except FileNotFoundError:
        print("Error: Page not found!")
    return html_page
    
def is_touch_invalid(fencer_id):
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

def get_score(id):
    fencer_score_file = 'fencer#' + id + "_score.txt"
    try:
        with open( fencer_score_file , 'r' ) as fle:
            score = int( fle.readline() )
    except FileNotFoundError:
        score = 0
    return score

def score_point(fencer_id):
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

def reset_score(fencer_id):
    fencer_score_file = 'fencer#' + fencer_id + "_score.txt"
    try:
        os.remove(fencer_score_file)
    except FileNotFoundError:
        print("No score file found, that's ok")
