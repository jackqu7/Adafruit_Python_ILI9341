import time

from .ILI9341 import ILI9341

INITR_GREENTAB  = 0x0
INITR_REDTAB    = 0x1
INITR_BLACKTAB  = 0x2

INITR_18GREENTAB    = INITR_GREENTAB
INITR_18REDTAB      = INITR_REDTAB
INITR_18BLACKTAB    = INITR_BLACKTAB
INITR_144GREENTAB   = 0x1

ST7735_TFTWIDTH  = 128
ST7735_TFTHEIGHT = 160

ST7735_NOP      = 0x00
ST7735_SWRESET  = 0x01
ST7735_RDDID    = 0x04
ST7735_RDDST    = 0x09

ST7735_SLPIN    = 0x10
ST7735_SLPOUT   = 0x11
ST7735_PTLON    = 0x12
ST7735_NORON    = 0x13

ST7735_INVOFF   = 0x20
ST7735_INVON    = 0x21
ST7735_DISPOFF  = 0x28
ST7735_DISPON   = 0x29
ST7735_CASET    = 0x2A
ST7735_RASET    = 0x2B
ST7735_RAMWR    = 0x2C
ST7735_RAMRD    = 0x2E

ST7735_PTLAR    = 0x30
ST7735_COLMOD   = 0x3A
ST7735_MADCTL   = 0x36

ST7735_FRMCTR1  = 0xB1
ST7735_FRMCTR2  = 0xB2
ST7735_FRMCTR3  = 0xB3
ST7735_INVCTR   = 0xB4
ST7735_DISSET5  = 0xB6

ST7735_PWCTR1   = 0xC0
ST7735_PWCTR2   = 0xC1
ST7735_PWCTR3   = 0xC2
ST7735_PWCTR4   = 0xC3
ST7735_PWCTR5   = 0xC4
ST7735_VMCTR1   = 0xC5

ST7735_RDID1    = 0xDA
ST7735_RDID2    = 0xDB
ST7735_RDID3    = 0xDC
ST7735_RDID4    = 0xDD

ST7735_PWCTR6   = 0xFC

ST7735_GMCTRP1  = 0xE0
ST7735_GMCTRN1  = 0xE1

ST7735_BLACK    = 0x0000
ST7735_BLUE     = 0x001F
ST7735_RED      = 0xF800
ST7735_GREEN    = 0x07E0
ST7735_CYAN     = 0x07FF
ST7735_MAGENTA  = 0xF81F
ST7735_YELLOW   = 0xFFE0
ST7735_WHITE    = 0xFFFF


class ST37735(ILI9341):

    def __init__(self, dc, spi, rst=None, gpio=None, width=ST7735_TFTWIDTH,
                 height=ST7735_TFTHEIGHT, clock=8000000):
        super(ST37735, self).__init__(dc, spi, rst=rst, gpio=gpio, width=width,
                                      height=height, clock=clock)

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        """Set the pixel address window for proceeding drawing commands. x0 and
        x1 should define the minimum and maximum x pixel bounds.  y0 and y1
        should define the minimum and maximum y pixel bound.  If no parameters
        are specified the default will be to update the entire display from 0,0
        to 239,319.
        """
        if x1 is None:
            x1 = self.width-1
        if y1 is None:
            y1 = self.height-1
        self.command(ST7735_CASET)      # Column addr set
        self.data(0x00)
        self.data(x0)                   # XSTART
        self.data(0x00)
        self.data(x1)                   # XEND
        self.command(ST7735_RASET)      # Row addr set
        self.data(0x00)
        self.data(y0)                   # YSTART
        self.data(0x00)
        self.data(y1)                   # YEND
        self.command(ST7735_RAMWR)      # write to RAM

    def reset(self):
        """Reset the display, if reset pin is connected."""
        if self._rst is not None:
            self._gpio.set_high(self._rst)
            time.sleep(0.5)
            self._gpio.set_low(self._rst)
            time.sleep(0.5)
            self._gpio.set_high(self._rst)
            time.sleep(0.5)

    def _init(self):
        # Part 1
        self.command(ST7735_SWRESET)
        time.sleep(0.15)
        self.command(ST7735_SLPOUT)
        time.sleep(0.5)
        self.command(ST7735_FRMCTR1)
        self.data(0x01)
        self.data(0x2C)
        self.data(0x2D)
        self.command(ST7735_FRMCTR2)
        self.data(0x01)
        self.data(0x2C)
        self.data(0x2D)
        self.command(ST7735_FRMCTR3)
        self.data(0x01)
        self.data(0x2C)
        self.data(0x2D)
        self.data(0x01)
        self.data(0x2C)
        self.data(0x2D)
        self.command(ST7735_INVCTR)
        self.data(0x07)
        self.command(ST7735_PWCTR1)
        self.data(0xA2)
        self.data(0x02)
        self.data(0x84)
        self.command(ST7735_PWCTR2)
        self.data(0xC5)
        self.command(ST7735_PWCTR3)
        self.data(0x0A)
        self.data(0x00)
        self.command(ST7735_PWCTR4)
        self.data(0x8A)
        self.data(0x2A)
        self.command(ST7735_PWCTR5)
        self.data(0x8A)
        self.data(0xEE)
        self.command(ST7735_VMCTR1)
        self.data(0x0E)
        self.command(ST7735_INVOFF)
        self.command(ST7735_MADCTL)
        self.data(0xC8)
        self.command(ST7735_COLMOD)
        self.data(0x05)

        # Part 2 (red)
        self.command(ST7735_CASET)
        self.data(0x00)
        self.data(0x00)
        self.data(0x00)
        self.data(0x7F)
        self.command(ST7735_RASET)
        self.data(0x00)
        self.data(0x00)
        self.data(0x00)
        self.data(0x9F)

        # Part 3
        self.command(ST7735_GMCTRP1)
        self.data(0x02)
        self.data(0x1C)
        self.data(0x07)
        self.data(0x12)
        self.data(0x37)
        self.data(0x32)
        self.data(0x29)
        self.data(0x2D)
        self.data(0x29)
        self.data(0x25)
        self.data(0x2B)
        self.data(0x39)
        self.data(0x00)
        self.data(0x01)
        self.data(0x03)
        self.data(0x10)
        self.command(ST7735_GMCTRN1)
        self.data(0x03)
        self.data(0x1D)
        self.data(0x07)
        self.data(0x06)
        self.data(0x2E)
        self.data(0x2C)
        self.data(0x29)
        self.data(0x2D)
        self.data(0x2E)
        self.data(0x2E)
        self.data(0x37)
        self.data(0x3F)
        self.data(0x00)
        self.data(0x00)
        self.data(0x02)
        self.data(0x10)
        self.command(ST7735_NORON)
        time.sleep(0.01)
        self.command(ST7735_DISPON)
        time.sleep(0.1)

        # Black tab
        self.command(ST7735_MADCTL)
        self.data(0xC0)










