import sys
import time
import serial
import binascii

from flask import Flask
from flask import request
from gpiozero import LED
from time import sleep

app       = Flask(__name__)
redLED    = LED(16)
yellowLED = LED(20)
greenLED  = LED(21)

try:
	ser = serial.Serial(
        	port     = '/dev/ttyUSB0',
        	baudrate = 9600,
        	parity   = serial.PARITY_NONE,
        	stopbits = serial.STOPBITS_ONE,
        	bytesize = serial.EIGHTBITS,
        	timeout  = None
		)
except:
	print('Cannot open USB port.', file=sys.stderr)	

colors = {
'red'       : '\x31',
'green'     : '\x32',
'amber'     : '\x33',
'dim red'   : '\x34',
'dim green' : '\x35',
'brown'     : '\x36',
'orange'    : '\x37',
'yellow'    : '\x38',
'rainbow'   : '\x39',
'rainbow 2' : '\x41',
'mixed'     : '\x42',
'auto'      : '\x43'
}

modes = {
'rotate'     : '\x61',
'hold'       : '\x62',
'flash'      : '\x63',
'scroll'     : '\x6d',
'auto'       : '\x6f',
'compressed' : '\x74'
}


@app.route('/')
def index():
    return 'Welcome to the traffic light API end point.'

@app.route('/control')
def control():
	signals = request.args.get('signals', '')

	message = request.args.get('message', '')
	mode = request.args.get('mode','rotate')
	color = request.args.get('color', 'rainbow')

	data = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x5a\x30\x30\x02\x41\x41\x1b\x30\x61'+'\x1b\x20'+modes[mode]+'\x1c'+colors[color]+message+'\x04'
	bytes_written = ser.write(data.encode('utf-8'))


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

	return 'recieved signals:  '+ signals + ' and message: ' + message;

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=80)
    
