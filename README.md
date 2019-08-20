![Alt Text](https://github.com/Joapfel/Mercedes-Benz-Connected-Vehicle-Chatbot/tires.gif)

# Mercedes-Benz Connected Vehicle Chatbot
A Houndify based chatbot which supports self defined Mercedes-Benz usecases using the Connected Vehicle API.

## How to start the Application
Run **python client_main.py**, the file is located in the top level directory.

## Usage
The application should be self explanatory:
- one can chat by typing into the textbox at the bottom
- one can speek to the system after clicking on the buttom with the microphone symbol
- (TTS is not supported yet)

## Dependencies
- The application uses **pyaudio** which is based on **portAudio** (needs to be installed on the OS).
- **QT5** should be installed such that it can be used by the **PyQt5** python package
- for the other dependencies it should be sufficient to **pip install requirements.txt**

## Usecases
Mercedes-Benz specific usecases exploit the Connected Vehicle API, therefore the following car domains are supported:
- information about tires, doors, location, odometer, fuel, state of charge
- command to (UN)LOCK doors

The information requests are specified as generic as possible on Houndify, therefore a sentence like
- "What is the status of my < car-domain >" 
- "Could you given me information about my < car-domain >"
- "How are/is my < car-domain >"

should work for tires, doors, fuel, etc.

For locking the doors try:
- "please tell Mercedes to lock my car"

## Implementation approach
From a technical perspective five steps had to be done:
- employing the Houndify SDK/API (TextClient & AudioClient)
- defining custom Mercedes-Benz Connected Car usecases on Houndify
- building a python wrapper for the Mercedes-Benz Connected Car REST API and define how to present the vehicle specific usecases to the user
- building the GUI with QT5 (QT5 Designer for the basic static layout and PyQt5 to add chat bubbles dynamically at runtime)
- and of course putting everything together (includes debugging, logging, getting crazy here and there ;) )
