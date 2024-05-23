"""
Raspberry Pi Pico/MicroPython exercise
240x240 ST7789 SPI LCD
using MicroPython library:
https://github.com/russhughes/st7789py_mpy

"""

import uos
import machine
from machine import Pin
import st7789py as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random


#Defines für das Display
display_CS = 13
display_DC = 16
display_RES = 12
display_SDA = 15
display_SCL = 14

#SPI(1) default pins
spi1_sck=14
spi1_mosi=15
spi1_miso=8     #not use
st7789_res = 12
st7789_dc  = 16
disp_width = 240
disp_height = 280
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)

print(uos.uname())
spi1 = machine.SPI(1, baudrate=1000000 ,sck=Pin(display_SCL), mosi=Pin(display_SDA), polarity=1, phase=1)
print(spi1)

display = st7789.ST7789(spi1, disp_width, disp_height,
                        reset=machine.Pin(st7789_res, machine.Pin.OUT),
                        dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                        rotation=2,
                        cs=machine.Pin(display_CS, machine.Pin.OUT))
# xstart=0, ystart=0,

#display.fill(st7789.color565(0, 255, 255))
'''
for r in range(2):
    display.fill(st7789.color565(r*125, 255, 0))
    print ("tst")
r_width = disp_width-20
r_height = disp_height-20
for g in range(255):
    display.fill_rect(10, 10, r_width, r_height, st7789.color565(0, g, 0))
    
r_width = disp_width-40
r_height = disp_height-40
for b in range(255):
    display.fill_rect(20, 20, r_width, r_height, st7789.color565(0, 0, b))

for i in range(255, 0, -1):
    display.fill(st7789.color565(i, i, i))

'''
display.fill(st7789.BLACK)
display.text(font2, "Hello World!", 10, 10)
display.text(font2, "Gigacard loft", 10, 40)
display.text(font2, "MicroPython", 10, 70)
display.text(font1, "ST7789 SPI 240*240 IPS", 10, 100)
display.text(font1, "https://github.com/", 10, 110)
display.text(font1, "russhughes/st7789py_mpy", 10, 120)
