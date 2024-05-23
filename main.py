from gigacardlib import Gigacard
from gigacardlib import Gcrotaryenc
from gigacardlib import Gcdisplay
import time

from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2

import italien_bild as bild

gigacard = Gigacard()
#gigacard._rotaryenc.startlistening()

#ADC test
#gigacard._DAC.set_voltage(0, 2)
#gigacard.setDACvoltage(0,2)

import machine
import utime
display = Gcdisplay()
#display.st7789.text(font2, "Hello World", 10, 10)
#display.st7789.bitmap(bild, 20, 20, 0)

display.st7789.bitmap(bild, 20, 20)
display.st7789.text(font1, "Italien urlaub jaa", 10, 130)
display.st7789.text(font1, "Schneaggchat for Gigacard bald", 0, 170)
#display.print_display("Gigacard")
#for x in range(25):
#    display.print_display("Zeile :" + str(x))    


gigacard._rotaryenc.stepsize = 50
gigacard._RGBLED._brightness = 1
'''
while True:
    print("Counter:", gigacard._rotaryenc.counter)
    #print("tastervalue", gigacard._rotaryenc.buttonpressed)
    gigacard.setRGBcolor(0,0,gigacard._rotaryenc.counter)
    
    if gigacard._rotaryenc.buttonpressed:
        gigacard.setRGBcolor(255,0,0)
    utime.sleep(0.1)  # kurze Pause zur Entlastung der CPU





gigacard.selftest()

#counter = 0
potistrom = 3.3/10000
while True:
    voltage = gigacard._ADC.read_ADC_mV(26)
    print("voltage", voltage)
    #print("Poti Widerstand",counter,voltage/potistrom)
    time.sleep(1)
    counter+= 1
    
'''

    
    


