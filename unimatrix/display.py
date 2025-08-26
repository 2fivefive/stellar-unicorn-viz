from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY
from stellar import StellarUnicorn

stellar = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)
stellar.set_brightness(0.3)
palette =[]

for i in range(6):
    palette.append(graphics.create_pen(32*i,42*i,21*i))
palette.reverse()
 
def draw(dots):
    graphics.set_pen(graphics.create_pen(0,0,0))
    graphics.clear()
    for x,y in dots:
        for i in range(6):
            graphics.set_pen(palette[i])
            graphics.pixel(x,y - i)
    stellar.update(graphics)
