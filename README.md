# trafficlight
Web based traffic light controller


The Trafficlight is live!  https://www.screencast.com/t/l18Bn953
 
The API to control the trafficlight is quite simple….
 
Open a browser (inside our network) and send a URL that looks like this….
http://trafficlight.ihire.local/control?signals=gYR...GyR...GYr...RGY
 
The letters and ‘,’ or ‘.’  do the following….
R = turns red off
r = turns red on
. = delay for 0.5 seconds
, = delay for .25 seconds
 
The example above will sequence through green, yellow, red (1.5 seconds apart) and then turn them all off.
 
I hope we can find creative ways to integrate this into our software build cycle, sales alert, alexa, or other clever idea!
 
Big thanks to Steve for the initial inspiration and buying the stop light.
Big thanks to David Marcus for the mounting brackets and wiring!
 
PS: Angola…now you have a way to make yourself know to the Frederick office…
Hello would be the following in morse code…
http://trafficlight.ihire.local/control?signals=RYG.r...R,r...R,r...R,r...R...y...Y...g...G,g,,,G,g...G,g...G,r...R,r,,,R,r...R,r...R,y,,,Y,y,,,Y,y,Y
 
Version 2.0 of the trafficlight now supports additional URL parameters to control the attached marquee. The Marquee is manufactured by BetaBrite and comes with a remote to program the marquee and with customer windows software. However, in the spirit of iHire innovation, we have hacked the BetaBrite sign and are using the raspberry pi to stream serial messages to the sign.  These commands will ride along the same request to the trafficlight to control them both.
 
Here are the updated command parameters:
 
signals - this is a sequence of characters to control the flashing of the red, yellow, and green traffic light.
R - turn RED light ON
r - turn RED light OFF
Y - Turn YELLOW light ON
y - Turn YELLOW light OFF
G- Turn GREEN light ON
g - Turn GREEN light OFF
, - Delay for a quarter second before the next signal
. - Delay for a half second before the next signal
message - this is the text message that you want to send to the sign (up to 150 characters). I believe certain characters (like '-') somehow need to be escaped..

color - the color of the text. Available colors are:
red
green
amber
dim red
dim green
brown
orange
yellow
rainbow
rainbow 2
mixed
auto

mode - this controls how the text is displayed. If the text is larger that the screen, the text will be split on word boundaries (if possible) and shown. Available modes are:
rotate - runs acrossed the screen from the right
hold - appears in the middle of the screen 
flash - words flash on the screen
scroll - words scroll up from the bottom
auto - a crazy combination of display types (this one is interesting)
compressed - compressed letters streaming in from the right.

http://trafficlight.ihire.local/control?signals=gYR...GyR...GYr...RGY&message=iHire is on fire.&color=rainbow&mode=compressed

