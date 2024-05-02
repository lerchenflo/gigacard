import machine
from machine import Pin

#Defines für das Display
display_CS = 13
display_DC = 16
display_RES = 12
display_SDA = 15
display_SCL = 14



cs=machine.Pin(display_CS, machine.Pin.OUT)

spi1 = machine.SPI(1, baudrate=40000000,sck=Pin(display_SCL), mosi=Pin(display_SDA), polarity=1)
print(spi1)

msg = bytearray()
msg.append(0x28)

cs.value(1)
spi1.write(msg)
cs.value(0)
print("sent: ", msg)