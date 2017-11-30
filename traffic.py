import sys
import time
import serial
import binascii

from flask import Flask
from flask import request
from flask import render_template
from gpiozero import LED
from time import sleep

#################################################
# Define the FLask main loop.
#################################################
app       = Flask(__name__)

#################################################
# Define the PGIO pins connected to the lights.
#################################################
redLED    = LED(16)
yellowLED = LED(20)
greenLED  = LED(21)

#################################################
# Open the serial port with the correct settings
# to communicate to the Betabrite marquee.
#################################################
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

################################################
# Define the various colors support by the sign.
# Each color is preceeded by the control code
# needed to set the color.
################################################
colors = {
'red'       : '\x1c\x31',
'green'     : '\x1c\x32',
'amber'     : '\x1c\x33',
'dim red'   : '\x1c\x34',
'dim green' : '\x1c\x35',
'brown'     : '\x1c\x36',
'orange'    : '\x1c\x37',
'yellow'    : '\x1c\x38',
'rainbow'   : '\x1c\x39',
'rainbow 2' : '\x1c\x41',
'mixed'     : '\x1c\x42',
'auto'      : '\x1c\x43'
}

################################################
# Define the various tet display modes. This 
# controls hold the text is displayted on the 
# sign.
################################################
modes = {
'rotate'     : '\x61',
'hold'       : '\x62',
'flash'      : '\x63',
'scroll'     : '\x6d',
'auto'       : '\x6f',
'compressed' : '\x74'
}

################################################
# Setup the default route.
################################################
@app.route('/')
def index():
    return render_template('index.html');

################################################
# user input
################################################
@app.route('/controlpanel')
def controlpanel():
        return render_template('control.html');

################################################
# help
################################################
@app.route('/help')
def help():
        return render_template('help.html');

###############################################
# This is the 'control' route, where the heavy
# lifting is done.
###############################################
@app.route('/control')
def control():

	####################################################
	# Process all the command parameters from the URL.
	####################################################
	signals = request.args.get('signals', '')

	message = request.args.get('message', '')
	mode    = request.args.get('mode','rotate')
	color   = request.args.get('color', 'rainbow')

	if signals != "":
		print( 'signals: ', signals, file=sys.stderr)
	if message != "":
		currentDateTime = time.strftime("%m/%d %H:%M", time.localtime())
		message = message.replace('{time}'    , currentDateTime)
		message = message.replace('%7Btime%7D', currentDateTime)
		message = message.replace('%7btime%7d', currentDateTime)
		print( 'time: '   , currentDateTime, file=sys.stderr)
		print( 'message: ', message, file=sys.stderr)
	if mode != "":
		print( 'mode:    ', mode,    file=sys.stderr)
	if color != "":	
		print( 'color:   ', color,   file=sys.stderr)

	####################################################
	# Setup the command sequence to send to the sign.
	####################################################
	data = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x5a\x30\x30\x02\x41\x41\x1b\x30\x61'+'\x1b\x20'+modes[mode]+colors[color]+message+'\x04'

	####################################################
	# If the 'message' is not blank, write the message 
	# commnd sequence to the marquee.
	####################################################	
	if message != "":                
		bytes_written = ser.write(data.encode('utf-8'))
		print( 'Message displayed.', file=sys.stderr)

	####################################################
	# If the 'signals' is not blank, send the signals to
	# the trafficlight GPIOs that control the relays.
	####################################################
	if signals != "":
		for c in signals:
			if c == 'r':
				redLED.on()
			elif c == 'R':            
				redLED.off()
			elif c == 'y':
				yellowLED.on()
			elif c == 'Y':
				yellowLED.off()
			elif c == 'g':
				greenLED.on()
			elif c == 'G':
				greenLED.off()
			elif c == ',':
				sleep(.1)
			elif c == '.':
				sleep(.25)
			elif c == '-':
				sleep(.5)

		print( 'Signal received and sent to trafficlight.', file=sys.stderr)

	####################################################
	# Print out a replay to indicate what we just did.
	####################################################
	return render_template('control.html');

#################################################################
# Start the main processing loop on port 80 in 'threaded' mode.
# This will ensure that each request is handled in its own thread.
#################################################################
if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=80)
    
