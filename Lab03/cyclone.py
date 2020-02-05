import RPi.GPIO as GPIO
import time

count = 0
hits = 0
delay_loop = .1
delay_bounce = 0.3
# Define callback
def hitFunction(channel):
  global hits		# hits needs to be global to write
  if count == 3 :
    hits = 1
    
# Setup GPIO pins using board numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Input Pins
buttonPin =16
GPIO.setup(buttonPin,GPIO.IN,pull_up_down = GPIO.PUD_UP)

# Output Pins
ledArr = [21, 22, 23, 24, 25, 26, 27]
GPIO.setup(ledArr[0],GPIO.OUT)
GPIO.setup(ledArr[1],GPIO.OUT)
GPIO.setup(ledArr[2],GPIO.OUT)
GPIO.setup(ledArr[3],GPIO.OUT)
GPIO.setup(ledArr[4],GPIO.OUT)
GPIO.setup(ledArr[5],GPIO.OUT)
GPIO.setup(ledArr[6],GPIO.OUT)

# Set Event Detect
GPIO.add_event_detect(buttonPin,GPIO.FALLING,callback=hitFunction, bouncetime=int(delay_bounce*1000))
 
# While loop
while hits == 0:
  #print(count)
  GPIO.output(ledArr[count],GPIO.HIGH)
  time.sleep(delay_loop)
  GPIO.output(ledArr[count],GPIO.LOW)
  count = count + 1
  if count > 6:
    count = 0
freq = 5
dc = 50
pwm = GPIO.PWM(ledArr[3],freq)
pwm.start(dc)
time.sleep(3.5)
GPIO.output(ledArr[3],GPIO.LOW)
