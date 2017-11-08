#from EmulatorGUI import GPIO
import RPi.GPIO as GPIO
import time
import threading
from random import randint

print ("RASPI ASYNC LEDS BY KONEY")
keep_executing=True
sleep_micro=0.01
sleep_minimum=0.02
sleep_shorter=0.06
sleep_short=0.07
sleep_medium=0.10
sleep_long=1.1
sleep_longer=2.4
sleep_maximum=4

#IO_ports=[14,15,18,23,24,25,8,7,11,9,10,22,27,17,4,3,2]
# MAPPING PHISICAL PORTS TO LEDS
tower_top=14
front_=15
side_red=[9,11,10]
side_green=[23,25,24]
bi_led_red=17
bi_led_green=18

#### SETUP #################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(tower_top,GPIO.OUT)
GPIO.output(tower_top,True)
GPIO.setup(bi_led_red,GPIO.OUT)
GPIO.output(bi_led_red,True)
GPIO.setup(bi_led_green,GPIO.OUT)
GPIO.output(bi_led_green,True)
for i in range(len(side_red)):
  GPIO.setup(side_red[i],GPIO.OUT)
  GPIO.output(side_red[i],True)
for i in range(len(side_green)):
  GPIO.setup(side_green[i],GPIO.OUT)
  GPIO.output(side_green[i],True)
time.sleep(sleep_long)
GPIO.output(tower_top,False)
GPIO.output(bi_led_red,False)
GPIO.output(bi_led_green,False)
for i in range(len(side_red)):
  GPIO.output(side_red[i],False)
for i in range(len(side_green)):
  GPIO.output(side_green[i],False)
#### END SETUP ###############

def prob_rnd(range_low,range_hi,probs_factor):
  internal_range=randint(probs_factor, range_hi);
  final_number=randint(range_low, internal_range);
  #print(final_number)
  return final_number

def tower():
 while keep_executing==True:
  loop_factor=prob_rnd(3, 11, 8)
  loop_mode=prob_rnd(1, 3, 1) #1 random #2 dec #3 inc
  sleep_factor=prob_rnd(0, 8, 5) #0,8,5
  #loop_mode=3
  if loop_mode == 1:
   #print("loop mode=rnd")
   for i in range(loop_factor):
    rand=randint(i, loop_factor)
    GPIO.output(tower_top,True)
    time.sleep(sleep_micro*rand)
    rand=randint(i, loop_factor)
    GPIO.output(tower_top,False)
    time.sleep(sleep_micro*rand)
  if loop_mode == 2:
   #print("loop mode=dec")
   for i in range(loop_factor*2):
     GPIO.output(tower_top,True)
     time.sleep(sleep_micro*i)
     GPIO.output(tower_top,False)
     time.sleep(sleep_micro*i)
     #print(sleep_micro*i)
  if loop_mode == 3:
   #print("loop mode=inc")
   for i in range(loop_factor*3):
     GPIO.output(tower_top,True)
     time.sleep(sleep_micro)
     GPIO.output(tower_top,False)
     time.sleep(sleep_micro*(loop_factor*3-i))
     #print(sleep_micro*(loop_factor*3-i))
  #sleep_factor=randint(0, 8)
  time.sleep(sleep_long*sleep_factor)
  pass
 return


def sides_multiple():
 flicker_ratio=3
 while keep_executing==True:
  actual_side=side_green
  for i in range(len(actual_side)-1):
   for k in range(flicker_ratio):
    GPIO.output(actual_side[i],True)
    time.sleep(sleep_shorter)
    GPIO.output(actual_side[i],False)
    time.sleep(sleep_short)
  GPIO.output(side_red[len(side_red)-1],True)
  time.sleep(sleep_micro)
  GPIO.output(side_green[len(side_green)-1],False)
  time.sleep(sleep_longer)

  actual_side=side_red
  for i in range(len(actual_side)-1):
   for k in range(flicker_ratio):
    GPIO.output(actual_side[i],True)
    time.sleep(sleep_shorter)
    GPIO.output(actual_side[i],False)
    time.sleep(sleep_short)
  GPIO.output(side_green[len(side_green)-1],True)
  time.sleep(sleep_micro)
  GPIO.output(side_red[len(side_red)-1],False)
  time.sleep(sleep_longer)
  pass
 return


def bicolor():
 while  keep_executing==True:
  GPIO.output(bi_led_green,False)
  GPIO.output(bi_led_red,True)
  time.sleep(sleep_long)
  GPIO.output(bi_led_red,False)
  GPIO.output(bi_led_green,True)
  time.sleep(sleep_long)
  pass
 return


## ASYNC EXECUTE ##
t_sides = threading.Thread(target=sides_multiple)
t_tower = threading.Thread(target=tower)
t_bicolor = threading.Thread(target=bicolor)
t_bicolor.start()
time.sleep(sleep_longer)
t_sides.start()
time.sleep(sleep_maximum)
t_tower.start()

import tty
import sys
import termios

print("ANY KEY TO QUIT...")
orig_settings = termios.tcgetattr(sys.stdin)

tty.setraw(sys.stdin)
x = 0
while x != chr(27): # ESC
 x=sys.stdin.read(1)[0]
 termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
 keep_executing=False
 print("EXIT")

 sys.exit()
 GPIO.cleanup()