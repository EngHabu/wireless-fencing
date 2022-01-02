## Dev environment 
To be able to run locally, prep your dev environment by installing fastAPI and uvicorn by running the following:
`pip install -r requirements.txt`

## Local Testing
To run the webserver: `make start-server`
To test, open the browser and use the web UI or APIs for testing
    record a touch: http://127.0.0.1:8000/touch?id=<FENCER_ID> (either 1 or 2 since there're only 2 players)
    start a new game: http://127.0.0.1:8000/newbout?fencer1_name=<FENCER1_NAME>&fencer2_name=<FENCER2_NAME>

## Development
pages/fencers.html - web interface to start a new game and input fencers names
pages/scoreboard.html - web interface for live scoreboard

## Known issues/Future imporvements
The fencers html needs to be updated to use the newgame API instead of using websockets.
After fencers info is entered, redirect the user to the live scoreboard.
Rendering a local gif images doesn't work, for now an online version is used.
Add a decrement score API.
Add a fencer class that encapsulates the id, name & score.
Prettier UI
Move css to a separate file
Handle bad input (fencer id not 1 or 2, score going above 15)
Fix sound