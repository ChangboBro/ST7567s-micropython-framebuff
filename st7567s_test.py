#ST7567s with framebuffer demo
from machine import Pin, I2C
from ST7567s import ST7567s
import time
#if there is an error like "OSError: [Errno 5] EIO", check your cable connection may fix that.
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400_000)#recommanded freq

#try tuning parameters addr,elecvolt,regratio .etc if your screen don't works properly.
#Addr is the I2C address of your screen, it may be set by screen vender to values among 0x38-0x3F.
lcd = ST7567s(i2c,addr=0x3F,elecvolt=0x28,regratio=0x04,invX=False,invY=True,invdisp=False)

while(True):
    #time.sleep(1)
    lcd.fill(0)
    lcd.text("Sitronix",0,0,1)
    lcd.text("ST7567s demo",0,8,1)
    lcd.text("Using",0,24,1)
    lcd.text("Micro Python",0,32,1)
    lcd.text("and framebuffer",0,40,1)
    lcd.text("Code by:",0,48,1)
    lcd.text("ChangboBro",0,56,1)
    stamp=time.ticks_ms()
    lcd.show()
    delta=time.ticks_ms()-stamp
    print("write buffer time:%d ms"%delta)
    time.sleep(2)
    lcd.fill(0)
    lcd.text("now running on:",0,0,1)
    lcd.text("RaspberryPi pico",0,8,1)
    lcd.text("AKA rp2040",0,16,1)
    stamp=time.ticks_ms()
    lcd.show()
    delta=time.ticks_ms()-stamp
    print("write buffer time:%d ms"%delta)
    time.sleep(2)
