## Local Testing
First, run the webserver `python .\main.py`
On a separate powershell window, run the following command to simulate a point 
```
$postParams = "id=1"
Invoke-WebRequest -Uri http://localhost:8080 -Method POST -Body $postParams
```