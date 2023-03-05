# ST7567s-micropython-framebuff

A simple micropython lib (class) to drive Sitronix ST7567s 128*64 dot matrix mono color screen, using framebuffer (a MicroPython-specific librarie)
ST7567s is very similar to ST7567, their internal register is identical, but ST7567s supports I2C interface while ST7567 just support SPI interface.
ST7567s's I2C interface need to send a control byte before every data byte, that's very inefficient, so this screen's is not able to achieve a high refresh rate.

The st7567s_test.py is demonstrating you how to use ST7567s.py, you can use the ST7567s.py file in your own project.

Tested on rasberry pi pico, may also works on other devices running micropython.
