# The Circuit

## Setting up Arduino IDE for development

1. Follow steps outlined [here](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) to add support for the ESP-WROOM-32 board to your Arduino IDE.
2. Install USB UART Drivers for your OS from [here](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)

## On ESP32
1. Create a file named `arduino/client_esp32/arduino_secrets.h` and write your wifi SSID and password in there as follows:
   
   ```cpp
   #define WIFI_SSID "<WIFI SSID>"
   #define WIFI_SECRET "<WIFI PASSWORD>"
   ```

2. Open `arduino/client_esp32/client_esp21.ino` in your Arduino IDE, choose the right board.
3. After pressing `Deploy`, make sure to press and hold on the `boot` button on the board to allow it to receive the new software from your IDE.