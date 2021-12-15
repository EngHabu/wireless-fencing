
#include "WiFi.h"
#include <HTTPClient.h>

//#include "arduino_secrets.h"
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
const char *ssid = "TheNetwork"; // your network SSID (name)
const char *pass = "P@$$w0rd";   // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;                // your network key Index number (needed only for WEP)

int status = WL_IDLE_STATUS;
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(74,125,232,128);  // numeric IP for Google (no DNS)
const char *server = "http://libki.local:31622"; // name address for Google (using DNS)
String userID = "1";

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;

// constants won't change. They're used here to set pin numbers:
const int buttonPin = 2; // the number of the pushbutton pin
const int ledPin = 13;   // the number of the LED pin

// variables will change:
int buttonState = 0; // variable for reading the pushbutton status

void initWiFi()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print('.');
    delay(1000);
  }

  Serial.println(WiFi.localIP());
}

void setup()
{
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);

  Serial.begin(115200);
  initWiFi();
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
}

int x = 1;

void loop()
{
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

  if (x < 10)
  {
    Serial.print("Sending point");
    reportPoint();
    Serial.print("Sent");
    x++;
  }

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH)
  {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    reportPoint();
  }
  else
  {
    // turn LED off:
    digitalWrite(ledPin, LOW);
  }
}

void reportPoint()
{
  HTTPClient http;

  // Your Domain name with URL path or IP address with path
  http.begin(server);

  // Specify content-type header
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  // Data to send with HTTP POST
  String httpRequestData = "id=" + userID;
  // Send HTTP POST request
  int httpResponseCode = http.POST(httpRequestData);

  /*
      // If you need an HTTP request with a content type: application/json, use the following:
      http.addHeader("Content-Type", "application/json");
      // JSON data to send with HTTP POST
      String httpRequestData = "{\"api_key\":\"" + apiKey + "\",\"field1\":\"" + String(random(40)) + "\"}";           
      // Send HTTP POST request
      int httpResponseCode = http.POST(httpRequestData);*/

  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);

  // Free resources
  http.end();
}