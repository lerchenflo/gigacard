from gigacardlib import Gcdisplay
import gigacardlib
import utime

# schriftarte importieren
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2

from movie import frame1 # Bilder importieren
from movie import frame2
from movie import frame3 
from movie import frame4 
from movie import frame5 
frames = [frame1, frame2, frame3, frame4, frame5 ]

display = Gcdisplay() # Display initzialisieren
display.st7789.fill(gigacardlib.color565(0, 0, 50))

#display.st7789.bitmap(frame1, 50, 50)
display.st7789.text(font2, "Film Stickman von Fabi", 10, 10)
utime.sleep(0.5)
for i in range(5):
    print("printing frame: " + str(i))
    display.st7789.bitmap(frames[i], 50, 50)
    utime.sleep(0.2)
    
utime.sleep(0.5)# mehr warten
display.st7789.fill(gigacardlib.color565(255, 0, 0))
display.st7789.text(font2, "The End", 60, 100)
    

    