from flask import Flask
from flask import request
from gpiozero import LED
from time import sleep

app       = Flask(__name__)
redLED    = LED(16)
yellowLED = LED(20)
greenLED  = LED(21)

@app.route('/')
def index():
    return 'Welcome to the traffic light API end point.'

@app.route('/control')
def control():
    signals = request.args.get('signals', '')
    for c in signals:
        if c == 'R':
            redLED.on()
        elif c == 'r':
            redLED.off()
        elif c == 'Y':
            yellowLED.on()
        elif c == 'y':
            yellowLED.off()
        elif c == 'G':
            greenLED.on()
        elif c == 'g':
            greenLED.off()
        elif c == ',':
            sleep(.1)
        elif c == '.':
            sleep(.25)
        elif c == '-':
            sleep(.5)

    return 'recieved signals:  '+ signals;

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=80)

root@raspberrypi:/home/pi/dev/trafficlight#
