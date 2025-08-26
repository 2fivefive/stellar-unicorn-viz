from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY
from stellar import StellarUnicorn

stellar = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)
stellar.set_brightness(0.3)

palette =[
     graphics.create_pen(192,255,128),
     graphics.create_pen(180,255,94),
     graphics.create_pen(142,204,78),
     graphics.create_pen(104,153,57),
     graphics.create_pen(76,102,38),
     graphics.create_pen(38,51,19)
]
    
def draw(dots):
    graphics.set_pen(graphics.create_pen(0,0,0))
    graphics.clear()
    for x,y in dots:
        for i in range(6):
            graphics.set_pen(palette[i])
            graphics.pixel(x,y - i)
    stellar.update(graphics)
        
