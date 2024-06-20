from gigacardlib import Gigacard
from gigacardlib import Gcrotaryenc
from gigacardlib import Gcdisplay
import time
import machine
import utime

from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2

#import italien_bild as bild

gc = Gigacard()



gc._display.st7789.text(font2, "Hello World", 10, 10)
gc.printf("RGB - LED - Test:")
gc.setRGBcolor(255,0,0)
gc.printf("LED - Test:")
gc.LEDtest()
gc.printf("DAC - Test:")
gc._DAC.generate_sinus()
gc.printf("LED - Helligkeit erhöhen:")
gc.setRGBbrightness(1)




while True:

    print("Counter:", gc._rotaryenc.counter)
    #print("tastervalue", gigacard._rotaryenc.buttonpressed)
    gigacard.setRGBcolor(0,0,gigacard._rotaryenc.counter)
    if gigacard._IO.getbuttonstatus(gc.taster_1):
        gc.setRGBcolor(0,0,255)
    
    if gc._rotaryenc.buttonpressed:
        gc.setRGBcolor(255,0,0)
    utime.sleep(0.1)  # kurze Pause zur Entlastung der CPU