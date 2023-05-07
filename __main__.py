from machine import Pin, SPI, I2C
import framebuf
import utime
import time

WF_PARTIAL_2IN13_V3= [
    0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x14,0x0,0x0,0x0,0x0,0x0,0x0,  
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
    0x22,0x17,0x41,0x00,0x32,0x36,
]

WS_20_30_2IN13_V3 = [ 
    0x80,0x4A,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x40,0x4A,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x80,0x4A,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x40,0x4A,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0xF,0x0,0x0,0x0,0x0,0x0,0x0,    
    0xF,0x0,0x0,0xF,0x0,0x0,0x2,    
    0xF,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,    
    0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,  
    0x22,0x17,0x41,0x0,0x32,0x36  
]

EPD_WIDTH       = 122
EPD_HEIGHT      = 250

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

class EPD_2in13_V3_Portrait(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        if EPD_WIDTH % 8 == 0:
            self.width = EPD_WIDTH
        else :
            self.width = (EPD_WIDTH // 8) * 8 + 8
        self.height = EPD_HEIGHT
        
        self.full_lut = WF_PARTIAL_2IN13_V3
        self.partial_lut = WS_20_30_2IN13_V3
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
        self.init()
    
    '''
    function :Change the pin state
    parameter:
        pin : pin
        value : state
    '''
    def digital_write(self, pin, value):
        pin.value(value)

    '''
    function : Read the pin state 
    parameter:
        pin : pin
    '''
    def digital_read(self, pin):
        return pin.value()

    '''
    function : The time delay function
    parameter:
        delaytime : ms
    '''
    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)
        
    '''
    function : Write data to SPI
    parameter:
        data : data
    '''
    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    '''
    function :Hardware reset
    parameter:
    '''
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)   

    '''
    function :send command
    parameter:
     command : Command register
    '''
    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)
    
    '''
    function :send data
    parameter:
     data : Write data
    '''
    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
    
    '''
    function :Wait until the busy_pin goes LOW
    parameter:
    '''
    def ReadBusy(self):
        print('busy')
        self.delay_ms(10)
        while(self.digital_read(self.busy_pin) == 1):      # 0: idle, 1: busy
            self.delay_ms(10)    
        print('busy release')
    
    '''
    function : Turn On Display
    parameter:
    '''
    def TurnOnDisplay(self):
        self.send_command(0x22)  # Display Update Control
        self.send_data(0xC7)
        self.send_command(0x20)  #  Activate Display Update Sequence    
        self.ReadBusy()
    
    '''
    function : Turn On Display Part
    parameter:
    '''
    def TurnOnDisplayPart(self):
        self.send_command(0x22)  # Display Update Control
        self.send_data(0x0F)     # fast:0x0c, quality:0x0f, 0xcf
        self.send_command(0x20)  # Activate Display Update Sequence 
        self.ReadBusy()
    
    '''
    function : Set lut
    parameter:
        lut : lut data
    '''
    def LUT(self, lut):
        self.send_command(0x32)
        self.send_data1(lut[0:153])
        self.ReadBusy()
    
    '''
    function : Send lut data and configuration
    parameter:
        lut : lut data 
    '''
    def LUT_by_host(self, lut):
        self.LUT(lut)             # lut
        self.send_command(0x3F)
        self.send_data(lut[153])
        self.send_command(0x03)   # gate voltage
        self.send_data(lut[154])
        self.send_command(0x04)   # source voltage
        self.send_data(lut[155])  # VSH
        self.send_data(lut[156])  # VSH2
        self.send_data(lut[157])  # VSL
        self.send_command(0x2C)   # VCOM
        self.send_data(lut[158])
    
    '''
    function : Setting the display window
    parameter:
        Xstart : X-axis starting position
        Ystart : Y-axis starting position
        Xend : End position of X-axis
        Yend : End position of Y-axis
    '''
    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        self.send_command(0x44)                #  SET_RAM_X_ADDRESS_START_END_POSITION
        self.send_data((Xstart >> 3) & 0xFF)
        self.send_data((Xend >> 3) & 0xFF)
        
        self.send_command(0x45)                #  SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
        self.send_data(Yend & 0xFF)
        self.send_data((Yend >> 8) & 0xFF)
        
    '''
    function : Set Cursor
    parameter:
        Xstart : X-axis starting position
        Ystart : Y-axis starting position
    '''
    def SetCursor(self, Xstart, Ystart):
        self.send_command(0x4E)             #  SET_RAM_X_ADDRESS_COUNTER
        self.send_data(Xstart & 0xFF)
        
        self.send_command(0x4F)             #  SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)

    '''
    function : Initialize the e-Paper register
    parameter:
    '''
    def init(self):
        print('init')
        self.reset()
        self.delay_ms(100)
        
        self.ReadBusy()
        self.send_command(0x12)  # SWRESET
        self.ReadBusy()
        
        self.send_command(0x01)  # Driver output control 
        self.send_data(0xf9)
        self.send_data(0x00)
        self.send_data(0x00)
        
        self.send_command(0x11)  #data entry mode 
        self.send_data(0x03)
        
        self.SetWindows(0, 0, self.width-1, self.height-1)
        self.SetCursor(0, 0)
        
        self.send_command(0x3C)  # BorderWaveform
        self.send_data(0x05)
        
        self.send_command(0x21) # Display update control
        self.send_data(0x00)
        self.send_data(0x80)
        
        self.send_command(0x18) # Read built-in temperature sensor
        self.send_data(0x80)
        
        self.ReadBusy()
        self.LUT_by_host(self.partial_lut)
       
    '''
    function : Clear screen
    parameter:
    '''
    def Clear(self):
        self.send_command(0x24)
        self.send_data1([0xff] * self.height * int(self.width / 8))
                
        self.TurnOnDisplay()    
    
    '''
    function : Sends the image buffer in RAM to e-Paper and displays
    parameter:
        image : Image data
    '''
    def display(self, image):
        self.send_command(0x24)
        self.send_data1(image)
                
        self.TurnOnDisplay()
    
    '''
    function : Refresh a base image
    parameter:
        image : Image data
    '''
    def Display_Base(self, image):
        self.send_command(0x24)
        self.send_data1(image)
                
        self.send_command(0x26)
        self.send_data1(image)
                
        self.TurnOnDisplay()
        
    '''
    function : Sends the image buffer in RAM to e-Paper and partial refresh
    parameter:
        image : Image data
    '''    
    def display_Partial(self, image):
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(1)
        self.digital_write(self.reset_pin, 1)
        
        self.LUT_by_host(self.full_lut)
        
        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x40)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        
        self.send_command(0x3C)
        self.send_data(0x80)
        
        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.ReadBusy()
        
        self.SetWindows(0,0,self.width-1,self.height-1)
        self.SetCursor(0,0)
        
        self.send_command(0x24)
        self.send_data1(image)

        self.TurnOnDisplayPart()
    
    '''
    function : Enter sleep mode
    parameter:
    '''
    def sleep(self):
        self.send_command(0x10) #enter deep sleep
        self.send_data(0x01)
        self.delay_ms(100)
        

class EPD_2in13_V3_Landscape(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        if EPD_WIDTH % 8 == 0:
            self.width = EPD_WIDTH
        else :
            self.width = (EPD_WIDTH // 8) * 8 + 8

        self.height = EPD_HEIGHT
        
        self.full_lut = WF_PARTIAL_2IN13_V3
        self.partial_lut = WS_20_30_2IN13_V3
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.height, self.width, framebuf.MONO_VLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)   

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        print('busy')
        self.delay_ms(10)
        while(self.digital_read(self.busy_pin) == 1):      # 0: idle, 1: busy
            self.delay_ms(10)    
        print('busy release')

    def TurnOnDisplay(self):
        self.send_command(0x22)  # Display Update Control
        self.send_data(0xC7)
        self.send_command(0x20)  #  Activate Display Update Sequence    
        self.ReadBusy()

    def TurnOnDisplayPart(self):
        self.send_command(0x22)  # Display Update Control
        self.send_data(0x0F)     # fast:0x0c, quality:0x0f, 0xcf
        self.send_command(0x20)  # Activate Display Update Sequence 
        self.ReadBusy()

    def LUT(self, lut):
        self.send_command(0x32)
        self.send_data1(lut[0:153])
        self.ReadBusy()

    def LUT_by_host(self, lut):
        self.LUT(lut)             # lut
        self.send_command(0x3F)
        self.send_data(lut[153])
        self.send_command(0x03)   # gate voltage
        self.send_data(lut[154])
        self.send_command(0x04)   # source voltage
        self.send_data(lut[155])  # VSH
        self.send_data(lut[156])  # VSH2
        self.send_data(lut[157])  # VSL
        self.send_command(0x2C)   # VCOM
        self.send_data(lut[158])

    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        self.send_command(0x44)                #  SET_RAM_X_ADDRESS_START_END_POSITION
        self.send_data((Xstart >> 3) & 0xFF)
        self.send_data((Xend >> 3) & 0xFF)
        
        self.send_command(0x45)                #  SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
        self.send_data(Yend & 0xFF)
        self.send_data((Yend >> 8) & 0xFF)

    def SetCursor(self, Xstart, Ystart):
        self.send_command(0x4E)             #  SET_RAM_X_ADDRESS_COUNTER
        self.send_data(Xstart & 0xFF)
        
        self.send_command(0x4F)             #  SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)

    def init(self):
        print('init')
        self.reset()
        self.delay_ms(100)
        
        self.ReadBusy()
        self.send_command(0x12)  # SWRESET
        self.ReadBusy()
        
        self.send_command(0x01)  # Driver output control 
        self.send_data(0xf9)
        self.send_data(0x00)
        self.send_data(0x00)
        
        self.send_command(0x11)  #data entry mode 
        self.send_data(0x07)
        
        self.SetWindows(0, 0, self.width-1, self.height-1)
        self.SetCursor(0, 0)
        
        self.send_command(0x3C)  # BorderWaveform
        self.send_data(0x05)
        
        self.send_command(0x21) # Display update control
        self.send_data(0x00)
        self.send_data(0x80)
        
        self.send_command(0x18) # Read built-in temperature sensor
        self.send_data(0x80)
        
        self.ReadBusy()
        self.LUT_by_host(self.partial_lut)

    def Clear(self):
        self.send_command(0x24)
        self.send_data1([0xff] * self.height * int(self.width / 8))
                
        self.TurnOnDisplay()    

    def display(self, image):
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])

        self.TurnOnDisplay()

    def Display_Base(self, image):
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])
                
        self.send_command(0x26)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])
                
        self.TurnOnDisplay()
        
    def display_Partial(self, image):
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(1)
        self.digital_write(self.reset_pin, 1)
        
        self.LUT_by_host(self.full_lut)
        
        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x40)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        
        self.send_command(0x3C)
        self.send_data(0x80)
        
        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.ReadBusy()
        
        self.SetWindows(0,0,self.width-1,self.height-1)
        self.SetCursor(0,0)
        
        self.send_command(0x24)
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(0, self.height):
                self.send_data(image[i + j * self.height])
                
        self.TurnOnDisplayPart()
    
    def sleep(self):
        self.send_command(0x10) #enter deep sleep
        self.send_data(0x01)
        self.delay_ms(100)
        
    # Config Register (R/W)
_REG_CONFIG                 = 0x00
# SHUNT VOLTAGE REGISTER (R)
_REG_SHUNTVOLTAGE           = 0x01

# BUS VOLTAGE REGISTER (R)
_REG_BUSVOLTAGE             = 0x02

# POWER REGISTER (R)
_REG_POWER                  = 0x03

# CURRENT REGISTER (R)
_REG_CURRENT                = 0x04

# CALIBRATION REGISTER (R/W)
_REG_CALIBRATION            = 0x05

class BusVoltageRange:
    """Constants for ``bus_voltage_range``"""
    RANGE_16V               = 0x00      # set bus voltage range to 16V
    RANGE_32V               = 0x01      # set bus voltage range to 32V (default)

class Gain:
    """Constants for ``gain``"""
    DIV_1_40MV              = 0x00      # shunt prog. gain set to  1, 40 mV range
    DIV_2_80MV              = 0x01      # shunt prog. gain set to /2, 80 mV range
    DIV_4_160MV             = 0x02      # shunt prog. gain set to /4, 160 mV range
    DIV_8_320MV             = 0x03      # shunt prog. gain set to /8, 320 mV range

class ADCResolution:
    """Constants for ``bus_adc_resolution`` or ``shunt_adc_resolution``"""
    ADCRES_9BIT_1S          = 0x00      #  9bit,   1 sample,     84us
    ADCRES_10BIT_1S         = 0x01      # 10bit,   1 sample,    148us
    ADCRES_11BIT_1S         = 0x02      # 11 bit,  1 sample,    276us
    ADCRES_12BIT_1S         = 0x03      # 12 bit,  1 sample,    532us
    ADCRES_12BIT_2S         = 0x09      # 12 bit,  2 samples,  1.06ms
    ADCRES_12BIT_4S         = 0x0A      # 12 bit,  4 samples,  2.13ms
    ADCRES_12BIT_8S         = 0x0B      # 12bit,   8 samples,  4.26ms
    ADCRES_12BIT_16S        = 0x0C      # 12bit,  16 samples,  8.51ms
    ADCRES_12BIT_32S        = 0x0D      # 12bit,  32 samples, 17.02ms
    ADCRES_12BIT_64S        = 0x0E      # 12bit,  64 samples, 34.05ms
    ADCRES_12BIT_128S       = 0x0F      # 12bit, 128 samples, 68.10ms

class Mode:
    """Constants for ``mode``"""
    POWERDOW                = 0x00      # power down
    SVOLT_TRIGGERED         = 0x01      # shunt voltage triggered
    BVOLT_TRIGGERED         = 0x02      # bus voltage triggered
    SANDBVOLT_TRIGGERED     = 0x03      # shunt and bus voltage triggered
    ADCOFF                  = 0x04      # ADC off
    SVOLT_CONTINUOUS        = 0x05      # shunt voltage continuous
    BVOLT_CONTINUOUS        = 0x06      # bus voltage continuous
    SANDBVOLT_CONTINUOUS    = 0x07      # shunt and bus voltage continuous
 
class INA219:
    def __init__(self, i2c_bus=1, addr=0x40):
        self.i2c = I2C(i2c_bus);
        self.addr = addr

        # Set chip to known config values to start
        self._cal_value = 0
        self._current_lsb = 0
        self._power_lsb = 0
        self.set_calibration_32V_2A()
        
    def read(self,address):
        data = self.i2c.readfrom_mem(self.addr, address, 2)
        return ((data[0] * 256 ) + data[1])

    def write(self,address,data):
        temp = [0,0]
        temp[1] = data & 0xFF
        temp[0] =(data & 0xFF00) >> 8
        self.i2c.writeto_mem(self.addr,address,bytes(temp))

    def set_calibration_32V_2A(self):
        """Configures to INA219 to be able to measure up to 32V and 2A of current. Counter
           overflow occurs at 3.2A.
           ..note :: These calculations assume a 0.1 shunt ohm resistor is present
        """
        # By default we use a pretty huge range for the input voltage,
        # which probably isn't the most appropriate choice for system
        # that don't use a lot of power.  But all of the calculations
        # are shown below if you want to change the settings.  You will
        # also need to change any relevant register settings, such as
        # setting the VBUS_MAX to 16V instead of 32V, etc.

        # VBUS_MAX = 32V             (Assumes 32V, can also be set to 16V)
        # VSHUNT_MAX = 0.32          (Assumes Gain 8, 320mV, can also be 0.16, 0.08, 0.04)
        # RSHUNT = 0.1               (Resistor value in ohms)

        # 1. Determine max possible current
        # MaxPossible_I = VSHUNT_MAX / RSHUNT
        # MaxPossible_I = 3.2A

        # 2. Determine max expected current
        # MaxExpected_I = 2.0A

        # 3. Calculate possible range of LSBs (Min = 15-bit, Max = 12-bit)
        # MinimumLSB = MaxExpected_I/32767
        # MinimumLSB = 0.000061              (61uA per bit)
        # MaximumLSB = MaxExpected_I/4096
        # MaximumLSB = 0,000488              (488uA per bit)

        # 4. Choose an LSB between the min and max values
        #    (Preferrably a roundish number close to MinLSB)
        # CurrentLSB = 0.0001 (100uA per bit)
        self._current_lsb = 1  # Current LSB = 100uA per bit

        # 5. Compute the calibration register
        # Cal = trunc (0.04096 / (Current_LSB * RSHUNT))
        # Cal = 4096 (0x1000)

        self._cal_value = 4096

        # 6. Calculate the power LSB
        # PowerLSB = 20 * CurrentLSB
        # PowerLSB = 0.002 (2mW per bit)
        self._power_lsb = .002  # Power LSB = 2mW per bit

        # 7. Compute the maximum current and shunt voltage values before overflow
        #
        # Max_Current = Current_LSB * 32767
        # Max_Current = 3.2767A before overflow
        #
        # If Max_Current > Max_Possible_I then
        #    Max_Current_Before_Overflow = MaxPossible_I
        # Else
        #    Max_Current_Before_Overflow = Max_Current
        # End If
        #
        # Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
        # Max_ShuntVoltage = 0.32V
        #
        # If Max_ShuntVoltage >= VSHUNT_MAX
        #    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
        # Else
        #    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
        # End If

        # 8. Compute the Maximum Power
        # MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
        # MaximumPower = 3.2 * 32V
        # MaximumPower = 102.4W

        # Set Calibration register to 'Cal' calculated above
        self.write(_REG_CALIBRATION,self._cal_value)

        # Set Config register to take into account the settings above
        self.bus_voltage_range = BusVoltageRange.RANGE_32V
        self.gain = Gain.DIV_8_320MV
        self.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
        self.mode = Mode.SANDBVOLT_CONTINUOUS
        self.config = self.bus_voltage_range << 13 | \
                      self.gain << 11 | \
                      self.bus_adc_resolution << 7 | \
                      self.shunt_adc_resolution << 3 | \
                      self.mode
        self.write(_REG_CONFIG,self.config)
        
    def getShuntVoltage_mV(self):
        value = self.read(_REG_SHUNTVOLTAGE)
        if value > 32767:
            value -= 65535
        return value * 0.01
        
    def getBusVoltage_V(self):  
        self.read(_REG_BUSVOLTAGE)
        return (self.read(_REG_BUSVOLTAGE) >> 3) * 0.004
        
    def getCurrent_mA(self):
        value = self.read(_REG_CURRENT)
        if value > 32767:
            value -= 65535
        return value * self._current_lsb
    
    
if __name__=='__main__':
     
    # Create an ADS1115 ADC (16-bit) instance.
    ina219 = INA219(addr=0x43)
    epd = EPD_2in13_V3_Landscape()
    

    
    while True:
        epd.Clear()
        epd.fill(0xff)
    
        bus_voltage = ina219.getBusVoltage_V()             # voltage on V- (load side)
        current = ina219.getCurrent_mA()                   # current in mA
        P = (bus_voltage -3)/1.2*100
        if(P<0):P=0
        elif(P>100):P=100

        # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
        print("Voltage:  {:6.3f} V".format(bus_voltage))
        print("Current:  {:6.3f} A".format(current/1000))
        print("Percent:  {:6.1f} %".format(P))
        print("")
        epd.text("Percent:  {:6.1f} %".format(P), 0, 10, 0x00)
        epd.display(epd.buffer)
        time.sleep(5)