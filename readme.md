# Lorenz OS

## What is it?

This is a platform IO library meant to simplify project development for ESP8266 based boards.
It is therefore only compatible with ESP8266 with Arduino framework

## What can it do?

Currently, this OS features the following:

* Http-Server for browser interface
* Arduino-OTA running in the background (**hardcoded password**)
* A ntp client running in the background, providing local real-time while internet is present
* Interactive Serial interface that can be used to set the wifi credentials into the EEPROM using your USB connection
* Automatic Wifi reconnect every 30 seconds
* Handler to permanently store user specific parameters to EEPROM

Additionally, automatic build tools are added to the project during installation, which can be used to:

* Bind user http callback functions to ressources (like `/home`) in your header file, using only an attribute in your header file
* Schedule user functions to be called from loop with a specific interval, e.g. every 100 milliseconds, using only an attribute in your header file
* Automatically converts all `*.html` files from your project directory into raw c-strings, which can then be easily returned from the http-server

## What will be improved

* more documentation
