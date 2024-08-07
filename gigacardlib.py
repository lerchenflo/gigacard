#Gigacard Library V1

#Import für RGBLED
import neopixel
import machine
import time
import utime
import array
from math import sin, cos
import math
#from rotary import Rotary
from machine import Pin, SPI
#from ST7789 import ST7789

# import fonts for display
# todo: have fonts in same file
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2


# import for ST7789 driver

try:
    from time import sleep_ms
except ImportError:
    sleep_ms = lambda ms: None
    uint = int
    const = lambda x: x

    class micropython:
        @staticmethod
        def viper(func):
            return func

        @staticmethod
        def native(func):
            return func
import struct

#Defines für den Rotary Encoder
rotary_switch = 22
rotary_pinA = 20
rotary_pinB = 21

#Defines für das Display
display_CS = 13
display_DC = 16
display_RES = 12
display_SDA = 15
display_SCL = 14

disp_width = 240
disp_height = 280

#Defines für die ADCs
adc_poti = 26
adc_0 = 26
adc_1 = 27
adc_2 = 28
adc_3 = 29

#Defines für den DAC
dac_SCK = 18
dac_SDI = 19
dac_CS = 17

#Defines für die Taster
taster_1 = 8
taster_2 = 9
taster_3 = 10
taster_4 = 11

#Defines für die LEDs
led_1 = Pin(0,Pin.OUT)
led_2 = Pin(1,Pin.OUT)
led_3 = Pin(2,Pin.OUT)
led_4 = Pin(3,Pin.OUT)
led_5 = Pin(4,Pin.OUT)
led_6 = Pin(5,Pin.OUT)
led_7 = Pin(6,Pin.OUT)
led_8 = Pin(7,Pin.OUT)



class Gigacard():
    
    def __init__(self):
        #Display Library initialisieren
        
        
        #Rotary Encoder Library initialisieren
        
        self._rotaryenc = Gcrotaryenc()
        self._rotaryenc.startlistening()
        self._display = Gcdisplay()
        self._ADC = GcADC()
        self._DAC = GcDAC()
        self._RGBLED = GcRGBLED()
        self._IO = GcIO()
        print("Gigacard init fertig")
        

    def selftest(self):
        self._display.selftest()
        self.printf("RGB - LED - Test:")
        self._RGBLED.test()
        self.printf("LED - Test:")
        self.LEDtest()
        self.printf("DAC - Test:")
        self._DAC.generate_sinus(duration=100)
        

    #Testfunktion für die RGB - LED
    def RGBLEDtest(self):
        self._RGBLED.test()
        
    def setRGBcolor(self, Red, Green, Blue):
        self._RGBLED.setcolor(Red,Green,Blue)
    def setRGBbrightness(self, brightness):
        self._RGBLED.setbrightness(brightness)

    #Testfunktion für die 8 LEDs
    def LEDtest(self):
        led_pins = [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0]  # Pinnummern von 0 bis 7
        leds = [machine.Pin(pin, machine.Pin.OUT) for pin in led_pins]
        for i in range(2):
            for led in leds:
                led.on()
                time.sleep(0.2)  # Warte für eine Sekunde
                led.off()  # Schalte die LED aus

    #Display
    def cleardisplay(self):
        self._display.clear()
        
    def printf(self,text):
        self._display.print_display(text)
        
    def printf_xy(self,x, y, text):
        self._display.print_display_xy(x, y, text)

class Gcdisplay():
    #global st7789
    global linepx
    def __init__(self):
        self.spi1 = machine.SPI(1, baudrate=40000000 ,sck=Pin(display_SCL), mosi=Pin(display_SDA), polarity=1, phase=1)
        self.st7789 = ST7789(self.spi1, disp_width, disp_height,
                        reset=machine.Pin(display_RES, machine.Pin.OUT),
                        dc=machine.Pin(display_DC, machine.Pin.OUT),
                        rotation=2,
                        cs=machine.Pin(display_CS, machine.Pin.OUT))
        self.linepx = 15
        #st7789.fill(color565(0, 255, 255))
        #self.st7789.text(font1, "Hello World", 10, 100)
    def print_display(self, text):
        self.st7789.text(font1, text, 15, self.linepx)
        self.linepx += 10
        
    def print_display_xy(self, x, y, text):
        self.st7789.text(font1, text, y, x)
        
    def clear(self):
        self.st7789.clear()
        
    def selftest(self):
        self.print_display("test")
        

class Gcrotaryenc():
    global counter
    global buttonpressed
    
    #Funktion über dem Konstruktor, denn sie muss beim Ausführen des Konstruktors aufgerufen werden
    def startlistening(self):
        self.rotary_pinA.irq(handler=self.rotary_callback, trigger=machine.Pin.IRQ_FALLING)
        self.rotary_switch.irq(handler=self.switch_callback, trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING)
    
    
    def __init__(self, stepsize=1):
        self.inttime = 0
        self.buttonpressed = False
        self.counter = 0
        self.stepsize = stepsize
        self.rotary_pinA = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)
        self.rotary_pinB = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
        self.rotary_switch = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
        self.startlistening()
        

    # Funktion zur Überwachung der Drehrichtung
    def rotary_callback(self, pin):
        global counter
        global inttime
        if utime.ticks_diff(utime.ticks_ms(), self.inttime) > 100:
            if self.rotary_pinB.value():
                
                self.counter += self.stepsize
            else:
                self.counter -= self.stepsize
            self.inttime = utime.ticks_ms()
        
    def switch_callback(self, switch):
        global buttonpressed
        if self.rotary_switch.value():
            self.buttonpressed = False
        else:
            self.buttonpressed = True
        



class GcADC():
    def __init__(self):
        pass
    
    def read_ADC(self, ADCpin):
        
        analog_value = machine.ADC(machine.Pin(ADCpin))
        
        #Mittelwert über mehrere Messungen
        rounds = 20
        addedvoltage = 0
        for i in range(rounds):
            addedvoltage += analog_value.read_u16()
        return (addedvoltage / rounds) * (3300 / 65536)
        
class GcDAC():
    def __init__(self):
        self.spi = SPI(0, baudrate=400000, sck=Pin(dac_SCK, Pin.OUT), mosi=Pin(dac_SDI, Pin.OUT))
        # Define DAC chip select pin
        self.dac_cs = Pin(dac_CS, Pin.OUT)
        
        
    def set_voltage(self, channel, voltage, gain=None):
        command = 0x0000  # Start of command bits for channel 0 or 1
        
        # Channel selection & SHDN
        if channel == 0:
            command |= 0x1000  # Channel A
        elif channel == 1:
            command |= 0x9000  # Channel B
        else:
            raise ValueError("Invalid channel number. Should be 0 or 1.")
        
        v_ref = 2.048 # Reference Voltage
        
        # Autogain
        if gain == None and voltage > v_ref:
            gain = 2
        
        # gain selection
        if gain == None or gain == 1:
            command |= 0x2000 # Gain
        elif gain == 2:
            v_ref = v_ref * 2 # Gain x2
        else:
            raise ValueError("Invalid gain. Must be 1 or 2")
        
        if voltage < 0:
            raise ValueError("Voltage must be above 0")
        elif voltage > v_ref:
            raise ValueError("Voltage to high. Maybe use gain=2")
            
        # Convert voltage to 12-bit value (0 - 4095)
        value = int((voltage / v_ref) * 4095)  # Scale voltage to 12-bit value

        # Add data bits to command
        command |= value

        # Transmit command
        self.dac_cs.value(0)  # Set CS low to enable communication
        self.spi.write(bytes([(command >> 8) & 0xFF, command & 0xFF]))  # Send command bytes
        self.dac_cs.value(1)  # Set CS high to end communication


    def generate_sinus(self, amplitude=1, frequency=100, duration=30, sample_rate=2000, offset=0):
        self._amplitude = amplitude
        self._frequency = frequency
        self._duration = duration
        self._sample_rate = sample_rate
        self._offset = offset
        self._period = 1.0 / frequency
        self._samplecount = int(self._sample_rate * self._period)
        self.start_time = time.ticks_us()

        while time.ticks_diff(time.ticks_us(), self.start_time) < self._duration * 1_000_000:
            for i in range(self._samplecount):
                angle = 2 * math.pi * i / self._samplecount
                voltage = (self._amplitude / 2) * (1 + math.sin(angle)) + self._offset  # Offset hinzugefügt, um positive Spannung zu haben
                self.set_voltage(0, voltage)
                time.sleep(1 / self._sample_rate)

    def generate_sawtooth(self, amplitude=1, frequency=50, duration=20):
        self._amplitude = amplitude
        self._frequency = frequency
        self._duration = duration
        self._sample_rate = 1000
        self._period = 1.0 / frequency
        self._sample_count = int(self._sample_rate * self._period)
        self.start_time = time.ticks_us()

        while time.ticks_diff(time.ticks_us(), self.start_time) < duration * 1_000_000:
            for i in range(self._sample_count):
                voltage = (amplitude / self._sample_count) * i  # Lineare Zunahme von 0 bis Amplitude
                self.set_voltage(0, voltage)
                time.sleep(1 / self._sample_rate)

    def generate_pwm(self, amplitude=1, frequency=50, duration=20, dutycycle=50):
        if dutycycle > 100 or dutycycle < 0:
            raise ValueError("Impossible Dutycycle")
        
        
        self._amplitude = amplitude
        self._frequency = frequency
        self._duration = duration
        self._dutycycle = dutycycle
        self._period = 1 / frequency
        self.start_time = time.ticks_us()
        self.ontime = self._period * (dutycycle / 100) * 1_000_000  # in Mikrosekunden
        self.offtime = self._period * ((100 - dutycycle) / 100) * 1_000_000  # in Mikrosekunden

        while time.ticks_diff(time.ticks_us(), self.start_time) < self._duration * 1_000_000:
            #Wenn dutycycle 100 oder 0 ist
            if self._dutycycle == 100:
                self.set_voltage(0, self._amplitude)
            elif self._dutycycle == 0:
                self.set_voltage(0, 0)
            else:
                cycle_start_time = time.ticks_us()
            
                # Set voltage to high (amplitude)
                self.set_voltage(0, self._amplitude)
                # Wait for ontime duration
                while time.ticks_diff(time.ticks_us(), cycle_start_time) < self.ontime:
                    pass
            
                cycle_start_time = time.ticks_us()
            
                # Set voltage to low (0)
                self.set_voltage(0, 0)
                # Wait for offtime duration
                while time.ticks_diff(time.ticks_us(), cycle_start_time) < self.offtime:
                    pass
            
            
            
        
    
    
        
class GcIO():
    def __init__(self):
        self._button1 = machine.Pin(taster_1, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._button2 = machine.Pin(taster_2, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._button3 = machine.Pin(taster_3, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._button4 = machine.Pin(taster_4, machine.Pin.IN, machine.Pin.PULL_DOWN)
        
    
    def getbuttonstatus(self, button):
        if button == taster_1:
            return self._button1.value()
        elif button == taster_2:
            return self._button2.value()
        elif button == taster_3:
            return self._button3.value()
        elif button == taster_4:
            return self._button4.value()
        else:
            raise ValueError("Not available button selected")
    
    def set_pullup(self, pin):
        machine.Pin(pin, machine.Pin.PULL_UP)
        
    def set_pulldown(self, pin):
        machine.Pin(pin, machine.Pin.PULL_DOWN)

    def set_input(self, pin):
        machine.Pin(pin, machine.Pin.IN)

    def set_output(self, pin):
        machine.Pin(pin, machine.Pin.OUT)
        
    def set_highz(self, pin):
        machine.Pin(pin, machine.Pin.OPEN_DRAIN)


class GcRGBLED():
    
    def __init__(self, brightness = 0.01):
        PIN = machine.Pin(23,machine.Pin.PULL_DOWN)  # GPIO-Pin, an dem die Datenleitung der WS2812 angeschlossen ist
        self._brightness = brightness
        self._led = neopixel.NeoPixel(PIN, 1, bpp=3)
        self._lastcolor = array.array('i',[0,0,0])

    # Funktion zum setzen der Helligkeit
    def setbrightness(self, brightness):
        self._brightness = brightness
        self.setcolor(self._lastcolor[0], self._lastcolor[1], self._lastcolor[2])

    # Funktion zum Setzen einer Farbe auf der LED
    def setcolor(self,red, green, blue):
        self._led[0] = (int(round(red*self._brightness)), int(round(green*self._brightness)), int(round(blue*self._brightness)))
        self._led.write()
        self._lastcolor[0] = red
        self._lastcolor[1] = green
        self._lastcolor[2] = blue
    
    # Funktion zum Ausschalten der LED
    def off(self):
        self._led[0] = (0,0,0)
        self._led.write()
        self._lastcolor[0] = 0
        self._lastcolor[1] = 0
        self._lastcolor[2] = 0
    
    # Funktion für Weiße Farbe
    def white(self):
        self._led[0] = (255,255,255)
        self._led.write()
        self._lastcolor[0] = 255
        self._lastcolor[1] = 255
        self._lastcolor[2] = 255
        
    # Testfunktion
    def test(self):
        self.setcolor(255,0,0) # Rot
        time.sleep(0.5)
        self.setcolor(0,0,255) # Blau
        time.sleep(0.5)
        self.setcolor(0,255,0) # Grün
        time.sleep(0.5)
        self.setcolor(255,3,190) # Pink
        time.sleep(0.5)
        
        #Loop durch viele Farben -> Tipp: Nicht in die LED schauen sonst blind
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    self.setcolor(x*50,y*50,z*50)
                    time.sleep(0.06)
        self.off()
   
   
   
   
   
# ST7789 commands
_ST7789_SWRESET = b"\x01"
_ST7789_SLPIN = b"\x10"
_ST7789_SLPOUT = b"\x11"
_ST7789_NORON = b"\x13"
_ST7789_INVOFF = b"\x20"
_ST7789_INVON = b"\x21"
_ST7789_DISPOFF = b"\x28"
_ST7789_DISPON = b"\x29"
_ST7789_CASET = b"\x2a"
_ST7789_RASET = b"\x2b"
_ST7789_RAMWR = b"\x2c"
_ST7789_VSCRDEF = b"\x33"
_ST7789_COLMOD = b"\x3a"
_ST7789_MADCTL = b"\x36"
_ST7789_VSCSAD = b"\x37"
_ST7789_RAMCTL = b"\xb0"

# MADCTL bits
_ST7789_MADCTL_MY = const(0x80)
_ST7789_MADCTL_MX = const(0x40)
_ST7789_MADCTL_MV = const(0x20)
_ST7789_MADCTL_ML = const(0x10)
_ST7789_MADCTL_BGR = const(0x08)
_ST7789_MADCTL_MH = const(0x04)
_ST7789_MADCTL_RGB = const(0x00)

RGB = 0x00
BGR = 0x08

# Color modes
_COLOR_MODE_65K = const(0x50)
_COLOR_MODE_262K = const(0x60)
_COLOR_MODE_12BIT = const(0x03)
_COLOR_MODE_16BIT = const(0x05)
_COLOR_MODE_18BIT = const(0x06)
_COLOR_MODE_16M = const(0x07)

# Color definitions
BLACK = const(0x0000)
BLUE = const(0x001F)
RED = const(0xF800)
GREEN = const(0x07E0)
CYAN = const(0x07FF)
MAGENTA = const(0xF81F)
YELLOW = const(0xFFE0)
WHITE = const(0xFFFF)

_ENCODE_PIXEL = const(">H")
_ENCODE_PIXEL_SWAPPED = const("<H")
_ENCODE_POS = const(">HH")
_ENCODE_POS_16 = const("<HH")

# must be at least 128 for 8 bit wide fonts
# must be at least 256 for 16 bit wide fonts
_BUFFER_SIZE = const(256)

_BIT7 = const(0x80)
_BIT6 = const(0x40)
_BIT5 = const(0x20)
_BIT4 = const(0x10)
_BIT3 = const(0x08)
_BIT2 = const(0x04)
_BIT1 = const(0x02)
_BIT0 = const(0x01)

# fmt: off

# Rotation tables
#   (madctl, width, height, xstart, ystart, needs_swap)[rotation % 4]

_DISPLAY_240x320 = (
    (0x00, 240, 320, 0, 0, False),
    (0x60, 320, 240, 0, 0, False),
    (0xc0, 240, 320, 0, 0, False),
    (0xa0, 320, 240, 0, 0, False))

_DISPLAY_240x240 = (
    (0x00, 240, 240,  0,  0, False),
    (0x60, 240, 240,  0,  0, False),
    (0xc0, 240, 240,  0, 80, False),
    (0xa0, 240, 240, 80,  0, False))

_DISPLAY_240x280 = (
    (0x00, 240, 280,  0,  0, False),
    (0x60, 280, 240,  0,  0, False),
    (0xc0, 240, 280,  0,  20, False),
    (0xa0, 280, 240,  20,  0, False))

_DISPLAY_135x240 = (
    (0x00, 135, 240, 52, 40, False),
    (0x60, 240, 135, 40, 53, False),
    (0xc0, 135, 240, 53, 40, False),
    (0xa0, 240, 135, 40, 52, False))

_DISPLAY_128x128 = (
    (0x00, 128, 128, 2, 1, False),
    (0x60, 128, 128, 1, 2, False),
    (0xc0, 128, 128, 2, 1, False),
    (0xa0, 128, 128, 1, 2, False))

# index values into rotation table
_WIDTH = const(0)
_HEIGHT = const(1)
_XSTART = const(2)
_YSTART = const(3)
_NEEDS_SWAP = const(4)

# Supported displays (physical width, physical height, rotation table)
_SUPPORTED_DISPLAYS = (
    (240, 320, _DISPLAY_240x320),
    (240, 240, _DISPLAY_240x240),
    (240, 280, _DISPLAY_240x280),
    (135, 240, _DISPLAY_135x240),
    (128, 128, _DISPLAY_128x128))

# init tuple format (b'command', b'data', delay_ms)
_ST7789_INIT_CMDS = (
    ( b'\x11', b'\x00', 120),               # Exit sleep mode
    ( b'\x13', b'\x00', 0),                 # Turn on the display
    ( b'\xb6', b'\x0a\x82', 0),             # Set display function control
    ( b'\x3a', b'\x55', 10),                # Set pixel format to 16 bits per pixel (RGB565)
    ( b'\xb2', b'\x0c\x0c\x00\x33\x33', 0), # Set porch control
    ( b'\xb7', b'\x35', 0),                 # Set gate control
    ( b'\xbb', b'\x28', 0),                 # Set VCOMS setting
    ( b'\xc0', b'\x0c', 0),                 # Set power control 1
    ( b'\xc2', b'\x01\xff', 0),             # Set power control 2
    ( b'\xc3', b'\x10', 0),                 # Set power control 3
    ( b'\xc4', b'\x20', 0),                 # Set power control 4
    ( b'\xc6', b'\x0f', 0),                 # Set VCOM control 1
    ( b'\xd0', b'\xa4\xa1', 0),             # Set power control A
                                            # Set gamma curve positive polarity
    ( b'\xe0', b'\xd0\x00\x02\x07\x0a\x28\x32\x44\x42\x06\x0e\x12\x14\x17', 0),
                                            # Set gamma curve negative polarity
    ( b'\xe1', b'\xd0\x00\x02\x07\x0a\x28\x31\x54\x47\x0e\x1c\x17\x1b\x1e', 0),
    ( b'\x21', b'\x00', 0),                 # Enable display inversion
    ( b'\x29', b'\x00', 120)                # Turn on the display
)

def color565(red, green=0, blue=0):
    """
    Convert red, green and blue values (0-255) into a 16-bit 565 encoding.
    """
    if isinstance(red, (tuple, list)):
        red, green, blue = red[:3]
    return (red & 0xF8) << 8 | (green & 0xFC) << 3 | blue >> 3


class ST7789:
    """
    ST7789 driver class

    Args:
        spi (spi): spi object **Required**
        width (int): display width **Required**
        height (int): display height **Required**
        reset (pin): reset pin
        dc (pin): dc pin **Required**
        cs (pin): cs pin
        backlight(pin): backlight pin
        rotation (int):

          - 0-Portrait
          - 1-Landscape
          - 2-Inverted Portrait
          - 3-Inverted Landscape

        color_order (int):

          - RGB: Red, Green Blue, default
          - BGR: Blue, Green, Red

        custom_init (tuple): custom initialization commands

          - ((b'command', b'data', delay_ms), ...)

        custom_rotations (tuple): custom rotation definitions

          - ((width, height, xstart, ystart, madctl, needs_swap), ...)

    """

    def __init__(
        self,
        spi,
        width,
        height,
        reset=None,
        dc=None,
        cs=None,
        backlight=None,
        rotation=0,
        color_order=BGR,
        custom_init=None,
        custom_rotations=None,
    ):
        """
        Initialize display.
        """
        self.rotations = custom_rotations or self._find_rotations(width, height)
        if not self.rotations:
            supported_displays = ", ".join(
                [f"{display[0]}x{display[1]}" for display in _SUPPORTED_DISPLAYS]
            )
            raise ValueError(
                f"Unsupported {width}x{height} display. Supported displays: {supported_displays}"
            )

        if dc is None:
            raise ValueError("dc pin is required.")

        self.physical_width = self.width = width
        self.physical_height = self.height = height
        self.xstart = 0
        self.ystart = 0
        self.spi = spi
        self.reset = reset
        self.dc = dc
        self.cs = cs
        self.backlight = backlight
        self._rotation = rotation % 4
        self.color_order = color_order
        self.init_cmds = custom_init or _ST7789_INIT_CMDS
        self.hard_reset()
        # yes, twice, once is not always enough
        self.init(self.init_cmds)
        self.init(self.init_cmds)
        self.rotation(self._rotation)
        self.needs_swap = False
        self.fill(0x00)
        #print("Es display wurd inizialisiert")

        if backlight is not None:
            backlight.value(1)

    @staticmethod
    def _find_rotations(width, height):
        for display in _SUPPORTED_DISPLAYS:
            if display[0] == width and display[1] == height:
                return display[2]
        return None

    def init(self, commands):
        """
        Initialize display.
        """
        for command, data, delay in commands:
            self._write(command, data)
            sleep_ms(delay)

    def _write(self, command=None, data=None):
        """SPI write to the device: commands and data."""
        if self.cs:
            self.cs.off()
        if command is not None:
            self.dc.off()
            self.spi.write(command)
        if data is not None:
            self.dc.on()
            self.spi.write(data)
            if self.cs:
                self.cs.on()

    def hard_reset(self):
        """
        Hard reset display.
        """
        if self.cs:
            self.cs.off()
        if self.reset:
            self.reset.on()
        sleep_ms(10)
        if self.reset:
            self.reset.off()
        sleep_ms(10)
        if self.reset:
            self.reset.on()
        sleep_ms(120)
        if self.cs:
            self.cs.on()

    def soft_reset(self):
        """
        Soft reset display.
        """
        self._write(_ST7789_SWRESET)
        sleep_ms(150)

    def sleep_mode(self, value):
        """
        Enable or disable display sleep mode.

        Args:
            value (bool): if True enable sleep mode. if False disable sleep
            mode
        """
        if value:
            self._write(_ST7789_SLPIN)
        else:
            self._write(_ST7789_SLPOUT)

    def inversion_mode(self, value):
        """
        Enable or disable display inversion mode.

        Args:
            value (bool): if True enable inversion mode. if False disable
            inversion mode
        """
        if value:
            self._write(_ST7789_INVON)
        else:
            self._write(_ST7789_INVOFF)

    def rotation(self, rotation):
        """
        Set display rotation.

        Args:
            rotation (int):
                - 0-Portrait
                - 1-Landscape
                - 2-Inverted Portrait
                - 3-Inverted Landscape

            custom_rotations can have any number of rotations
        """
        rotation %= len(self.rotations)
        self._rotation = rotation
        (
            madctl,
            self.width,
            self.height,
            self.xstart,
            self.ystart,
            self.needs_swap,
        ) = self.rotations[rotation]

        if self.color_order == BGR:
            madctl |= _ST7789_MADCTL_BGR
        else:
            madctl &= ~_ST7789_MADCTL_BGR

        self._write(_ST7789_MADCTL, bytes([madctl]))

    def _set_window(self, x0, y0, x1, y1):
        """
        Set window to column and row address.

        Args:
            x0 (int): column start address
            y0 (int): row start address
            x1 (int): column end address
            y1 (int): row end address
        """
        if x0 <= x1 <= self.width and y0 <= y1 <= self.height:
            self._write(
                _ST7789_CASET,
                struct.pack(_ENCODE_POS, x0 + self.xstart, x1 + self.xstart),
            )
            self._write(
                _ST7789_RASET,
                struct.pack(_ENCODE_POS, y0 + self.ystart, y1 + self.ystart),
            )
            self._write(_ST7789_RAMWR)

    def vline(self, x, y, length, color):
        """
        Draw vertical line at the given location and color.

        Args:
            x (int): x coordinate
            Y (int): y coordinate
            length (int): length of line
            color (int): 565 encoded color
        """
        self.fill_rect(x, y, 1, length, color)

    def hline(self, x, y, length, color):
        """
        Draw horizontal line at the given location and color.

        Args:
            x (int): x coordinate
            Y (int): y coordinate
            length (int): length of line
            color (int): 565 encoded color
        """
        self.fill_rect(x, y, length, 1, color)

    def pixel(self, x, y, color):
        """
        Draw a pixel at the given location and color.

        Args:
            x (int): x coordinate
            Y (int): y coordinate
            color (int): 565 encoded color
        """
        self._set_window(x, y, x, y)
        self._write(
            None,
            struct.pack(
                _ENCODE_PIXEL_SWAPPED if self.needs_swap else _ENCODE_PIXEL, color
            ),
        )

    def blit_buffer(self, buffer, x, y, width, height):
        """
        Copy buffer to display at the given location.

        Args:
            buffer (bytes): Data to copy to display
            x (int): Top left corner x coordinate
            Y (int): Top left corner y coordinate
            width (int): Width
            height (int): Height
        """
        self._set_window(x, y, x + width - 1, y + height - 1)
        self._write(None, buffer)

    def rect(self, x, y, w, h, color):
        """
        Draw a rectangle at the given location, size and color.

        Args:
            x (int): Top left corner x coordinate
            y (int): Top left corner y coordinate
            width (int): Width in pixels
            height (int): Height in pixels
            color (int): 565 encoded color
        """
        self.hline(x, y, w, color)
        self.vline(x, y, h, color)
        self.vline(x + w - 1, y, h, color)
        self.hline(x, y + h - 1, w, color)

    def fill_rect(self, x, y, width, height, color):
        """
        Draw a rectangle at the given location, size and filled with color.

        Args:
            x (int): Top left corner x coordinate
            y (int): Top left corner y coordinate
            width (int): Width in pixels
            height (int): Height in pixels
            color (int): 565 encoded color
        """
        self._set_window(x, y, x + width - 1, y + height - 1)
        chunks, rest = divmod(width * height, _BUFFER_SIZE)
        pixel = struct.pack(
            _ENCODE_PIXEL_SWAPPED if self.needs_swap else _ENCODE_PIXEL, color
        )
        self.dc.on()
        if chunks:
            data = pixel * _BUFFER_SIZE
            for _ in range(chunks):
                self._write(None, data)
        if rest:
            self._write(None, pixel * rest)

    def fill(self, color):
        """
        Fill the entire FrameBuffer with the specified color.

        Args:
            color (int): 565 encoded color
        """
        self.fill_rect(0, 0, self.width, self.height, color)

    def line(self, x0, y0, x1, y1, color):
        """
        Draw a single pixel wide line starting at x0, y0 and ending at x1, y1.

        Args:
            x0 (int): Start point x coordinate
            y0 (int): Start point y coordinate
            x1 (int): End point x coordinate
            y1 (int): End point y coordinate
            color (int): 565 encoded color
        """
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx // 2
        ystep = 1 if y0 < y1 else -1
        while x0 <= x1:
            if steep:
                self.pixel(y0, x0, color)
            else:
                self.pixel(x0, y0, color)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

    def vscrdef(self, tfa, vsa, bfa):
        """
        Set Vertical Scrolling Definition.

        To scroll a 135x240 display these values should be 40, 240, 40.
        There are 40 lines above the display that are not shown followed by
        240 lines that are shown followed by 40 more lines that are not shown.
        You could write to these areas off display and scroll them into view by
        changing the TFA, VSA and BFA values.

        Args:
            tfa (int): Top Fixed Area
            vsa (int): Vertical Scrolling Area
            bfa (int): Bottom Fixed Area
        """
        self._write(_ST7789_VSCRDEF, struct.pack(">HHH", tfa, vsa, bfa))

    def vscsad(self, vssa):
        """
        Set Vertical Scroll Start Address of RAM.

        Defines which line in the Frame Memory will be written as the first
        line after the last line of the Top Fixed Area on the display

        Example:

            for line in range(40, 280, 1):
                tft.vscsad(line)
                utime.sleep(0.01)

        Args:
            vssa (int): Vertical Scrolling Start Address

        """
        self._write(_ST7789_VSCSAD, struct.pack(">H", vssa))

    @micropython.viper
    @staticmethod
    def _pack8(glyphs, idx: uint, fg_color: uint, bg_color: uint):
        buffer = bytearray(128)
        bitmap = ptr16(buffer)
        glyph = ptr8(glyphs)

        for i in range(0, 64, 8):
            byte = glyph[idx]
            bitmap[i] = fg_color if byte & _BIT7 else bg_color
            bitmap[i + 1] = fg_color if byte & _BIT6 else bg_color
            bitmap[i + 2] = fg_color if byte & _BIT5 else bg_color
            bitmap[i + 3] = fg_color if byte & _BIT4 else bg_color
            bitmap[i + 4] = fg_color if byte & _BIT3 else bg_color
            bitmap[i + 5] = fg_color if byte & _BIT2 else bg_color
            bitmap[i + 6] = fg_color if byte & _BIT1 else bg_color
            bitmap[i + 7] = fg_color if byte & _BIT0 else bg_color
            idx += 1

        return buffer

    @micropython.viper
    @staticmethod
    def _pack16(glyphs, idx: uint, fg_color: uint, bg_color: uint):
        """
        Pack a character into a byte array.

        Args:
            char (str): character to pack

        Returns:
            128 bytes: character bitmap in color565 format
        """

        buffer = bytearray(256)
        bitmap = ptr16(buffer)
        glyph = ptr8(glyphs)

        for i in range(0, 128, 16):
            byte = glyph[idx]

            bitmap[i] = fg_color if byte & _BIT7 else bg_color
            bitmap[i + 1] = fg_color if byte & _BIT6 else bg_color
            bitmap[i + 2] = fg_color if byte & _BIT5 else bg_color
            bitmap[i + 3] = fg_color if byte & _BIT4 else bg_color
            bitmap[i + 4] = fg_color if byte & _BIT3 else bg_color
            bitmap[i + 5] = fg_color if byte & _BIT2 else bg_color
            bitmap[i + 6] = fg_color if byte & _BIT1 else bg_color
            bitmap[i + 7] = fg_color if byte & _BIT0 else bg_color
            idx += 1

            byte = glyph[idx]
            bitmap[i + 8] = fg_color if byte & _BIT7 else bg_color
            bitmap[i + 9] = fg_color if byte & _BIT6 else bg_color
            bitmap[i + 10] = fg_color if byte & _BIT5 else bg_color
            bitmap[i + 11] = fg_color if byte & _BIT4 else bg_color
            bitmap[i + 12] = fg_color if byte & _BIT3 else bg_color
            bitmap[i + 13] = fg_color if byte & _BIT2 else bg_color
            bitmap[i + 14] = fg_color if byte & _BIT1 else bg_color
            bitmap[i + 15] = fg_color if byte & _BIT0 else bg_color
            idx += 1

        return buffer

    def _text8(self, font, text, x0, y0, fg_color=WHITE, bg_color=BLACK):
        """
        Internal method to write characters with width of 8 and
        heights of 8 or 16.

        Args:
            font (module): font module to use
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """

        for char in text:
            ch = ord(char)
            if (
                font.FIRST <= ch < font.LAST
                and x0 + font.WIDTH <= self.width
                and y0 + font.HEIGHT <= self.height
            ):
                if font.HEIGHT == 8:
                    passes = 1
                    size = 8
                    each = 0
                else:
                    passes = 2
                    size = 16
                    each = 8

                for line in range(passes):
                    idx = (ch - font.FIRST) * size + (each * line)
                    buffer = self._pack8(font.FONT, idx, fg_color, bg_color)
                    self.blit_buffer(buffer, x0, y0 + 8 * line, 8, 8)

                x0 += 8

    def _text16(self, font, text, x0, y0, fg_color=WHITE, bg_color=BLACK):
        """
        Internal method to draw characters with width of 16 and heights of 16
        or 32.

        Args:
            font (module): font module to use
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """

        for char in text:
            ch = ord(char)
            if (
                font.FIRST <= ch < font.LAST
                and x0 + font.WIDTH <= self.width
                and y0 + font.HEIGHT <= self.height
            ):
                each = 16
                if font.HEIGHT == 16:
                    passes = 2
                    size = 32
                else:
                    passes = 4
                    size = 64

                for line in range(passes):
                    idx = (ch - font.FIRST) * size + (each * line)
                    buffer = self._pack16(font.FONT, idx, fg_color, bg_color)
                    self.blit_buffer(buffer, x0, y0 + 8 * line, 16, 8)
            x0 += 16

    def text(self, font, text, x0, y0, color=WHITE, background=BLACK):
        """
        Draw text on display in specified font and colors. 8 and 16 bit wide
        fonts are supported.

        Args:
            font (module): font module to use.
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        fg_color = color if self.needs_swap else ((color << 8) & 0xFF00) | (color >> 8)
        bg_color = (
            background
            if self.needs_swap
            else ((background << 8) & 0xFF00) | (background >> 8)
        )

        if font.WIDTH == 8:
            self._text8(font, text, x0, y0, fg_color, bg_color)
        else:
            self._text16(font, text, x0, y0, fg_color, bg_color)

    def bitmap(self, bitmap, x, y, index=0):
        """
        Draw a bitmap on display at the specified column and row

        Args:
            bitmap (bitmap_module): The module containing the bitmap to draw
            x (int): column to start drawing at
            y (int): row to start drawing at
            index (int): Optional index of bitmap to draw from multiple bitmap
                module
        """
        width = bitmap.WIDTH
        height = bitmap.HEIGHT
        to_col = x + width - 1
        to_row = y + height - 1
        if self.width <= to_col or self.height <= to_row:
            return

        bitmap_size = height * width
        buffer_len = bitmap_size * 2
        bpp = bitmap.BPP
        bs_bit = bpp * bitmap_size * index  # if index > 0 else 0
        palette = bitmap.PALETTE
        needs_swap = self.needs_swap
        buffer = bytearray(buffer_len)

        for i in range(0, buffer_len, 2):
            color_index = 0
            for _ in range(bpp):
                color_index = (color_index << 1) | (
                    (bitmap.BITMAP[bs_bit >> 3] >> (7 - (bs_bit & 7))) & 1
                )
                bs_bit += 1

            color = palette[color_index]
            if needs_swap:
                buffer[i] = color & 0xFF
                buffer[i + 1] = color >> 8
            else:
                buffer[i] = color >> 8
                buffer[i + 1] = color & 0xFF

        self._set_window(x, y, to_col, to_row)
        self._write(None, buffer)

    def pbitmap(self, bitmap, x, y, index=0):
        """
        Draw a bitmap on display at the specified column and row one row at a time

        Args:
            bitmap (bitmap_module): The module containing the bitmap to draw
            x (int): column to start drawing at
            y (int): row to start drawing at
            index (int): Optional index of bitmap to draw from multiple bitmap
                module

        """
        width = bitmap.WIDTH
        height = bitmap.HEIGHT
        bitmap_size = height * width
        bpp = bitmap.BPP
        bs_bit = bpp * bitmap_size * index  # if index > 0 else 0
        palette = bitmap.PALETTE
        needs_swap = self.needs_swap
        buffer = bytearray(bitmap.WIDTH * 2)

        for row in range(height):
            for col in range(width):
                color_index = 0
                for _ in range(bpp):
                    color_index <<= 1
                    color_index |= (
                        bitmap.BITMAP[bs_bit // 8] & 1 << (7 - (bs_bit % 8))
                    ) > 0
                    bs_bit += 1
                color = palette[color_index]
                if needs_swap:
                    buffer[col * 2] = color & 0xFF
                    buffer[col * 2 + 1] = color >> 8 & 0xFF
                else:
                    buffer[col * 2] = color >> 8 & 0xFF
                    buffer[col * 2 + 1] = color & 0xFF

            to_col = x + width - 1
            to_row = y + row
            if self.width > to_col and self.height > to_row:
                self._set_window(x, y + row, to_col, to_row)
                self._write(None, buffer)

    def write(self, font, string, x, y, fg=WHITE, bg=BLACK):
        """
        Write a string using a converted true-type font on the display starting
        at the specified column and row

        Args:
            font (font): The module containing the converted true-type font
            s (string): The string to write
            x (int): column to start writing
            y (int): row to start writing
            fg (int): foreground color, optional, defaults to WHITE
            bg (int): background color, optional, defaults to BLACK
        """
        buffer_len = font.HEIGHT * font.MAX_WIDTH * 2
        buffer = bytearray(buffer_len)
        fg_hi = fg >> 8
        fg_lo = fg & 0xFF

        bg_hi = bg >> 8
        bg_lo = bg & 0xFF

        for character in string:
            try:
                char_index = font.MAP.index(character)
                offset = char_index * font.OFFSET_WIDTH
                bs_bit = font.OFFSETS[offset]
                if font.OFFSET_WIDTH > 1:
                    bs_bit = (bs_bit << 8) + font.OFFSETS[offset + 1]

                if font.OFFSET_WIDTH > 2:
                    bs_bit = (bs_bit << 8) + font.OFFSETS[offset + 2]

                char_width = font.WIDTHS[char_index]
                buffer_needed = char_width * font.HEIGHT * 2

                for i in range(0, buffer_needed, 2):
                    if font.BITMAPS[bs_bit // 8] & 1 << (7 - (bs_bit % 8)) > 0:
                        buffer[i] = fg_hi
                        buffer[i + 1] = fg_lo
                    else:
                        buffer[i] = bg_hi
                        buffer[i + 1] = bg_lo

                    bs_bit += 1

                to_col = x + char_width - 1
                to_row = y + font.HEIGHT - 1
                if self.width > to_col and self.height > to_row:
                    self._set_window(x, y, to_col, to_row)
                    self._write(None, buffer[:buffer_needed])

                x += char_width

            except ValueError:
                pass

    def write_width(self, font, string):
        """
        Returns the width in pixels of the string if it was written with the
        specified font

        Args:
            font (font): The module containing the converted true-type font
            string (string): The string to measure

        Returns:
            int: The width of the string in pixels

        """
        width = 0
        for character in string:
            try:
                char_index = font.MAP.index(character)
                width += font.WIDTHS[char_index]
            except ValueError:
                pass

        return width

    @micropython.native
    def polygon(self, points, x, y, color, angle=0, center_x=0, center_y=0):
        """
        Draw a polygon on the display.

        Args:
            points (list): List of points to draw.
            x (int): X-coordinate of the polygon's position.
            y (int): Y-coordinate of the polygon's position.
            color (int): 565 encoded color.
            angle (float): Rotation angle in radians (default: 0).
            center_x (int): X-coordinate of the rotation center (default: 0).
            center_y (int): Y-coordinate of the rotation center (default: 0).

        Raises:
            ValueError: If the polygon has less than 3 points.
        """
        if len(points) < 3:
            raise ValueError("Polygon must have at least 3 points.")

        if angle:
            cos_a = cos(angle)
            sin_a = sin(angle)
            rotated = [
                (
                    x
                    + center_x
                    + int(
                        (point[0] - center_x) * cos_a - (point[1] - center_y) * sin_a
                    ),
                    y
                    + center_y
                    + int(
                        (point[0] - center_x) * sin_a + (point[1] - center_y) * cos_a
                    ),
                )
                for point in points
            ]
        else:
            rotated = [(x + int((point[0])), y + int((point[1]))) for point in points]

        for i in range(1, len(rotated)):
            self.line(
                rotated[i - 1][0],
                rotated[i - 1][1],
                rotated[i][0],
                rotated[i][1],
                color,
            )