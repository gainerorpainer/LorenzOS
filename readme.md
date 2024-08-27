# Lorenz OS

## What is it?

This is a platform IO library meant to simplify project development for ESP8266 based boards.
It is therefore only compatible with ESP8266 with Arduino framework.

**Warning**: This is still in delevopment, if you are interested in the development, let me know!

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
* examples

## changelog

### 1.2.1

* changed the way how the `/version` mechanism works
  * removed buildnumbers, which would have the project rebuild each time
  * instead used build-date as auto-generated version subnumber
* added `/os` http ressource, which gives information about the OS like the hostname
* renamed headers to make it clear that they should not be included from externally
  
### 1.2.0

* **Breaking Change**: `serializable` can not be "read-only", which can be controlled by the passed attribute argument
* `serializable` classes can now state extension functions, which allows the user to add own fields to the codegenerated serialization

### 1.1.0

* **Breaking Change**: parameters are now changed to `serializable` with a more broad application

### 1.0.2

* Added codegenerator for parameters class - will auto generate code for serialize and deserialize of class with attribute
