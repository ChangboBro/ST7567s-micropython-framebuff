#Tested on GM12864-59N, You may need to tune some parameters when initialize object to get good results
#Author: ChangboBro
#last edited on: 2023 Mar 4th
#internal register is the same as ST7567, the only difference is the interface.
#the I2C interface need a control byte before every sent byte, very low efficient, hard to get a high refresh rate.
from micropython import const
import framebuf

SET_BIAS  =const(0xA2)
POWER_CTRL=const(0x28)#|0x04/0x06/0x07
SET_BOOST =const(0xF8)
SOFT_RST  =const(0xE2)
SEG_DIR   =const(0xA0)#|0x01
COM_DIR   =const(0xC0)#|0x08
REGU_RATIO=const(0x20)#|0x00~0x07
EVSET_MODE=const(0x81)#MUST followed by 0x00~0x3F
DISP_ONOFF=const(0xAE)#|0x00/0x01
INV_DISP  =const(0xA6)#|0x00/0x01
ALL_PIX_ON=const(0xA4)
SRTLIN_SET=const(0x40)#40~7F
PAGEAD_SET=const(0xB0)#b0~b8
COLHAD_SET=const(0x10)#0x10~0x1F
COLLAD_SET=const(0x00)#0x00~0x0F

class ST7567s(framebuf.FrameBuffer):
    def __init__(self,i2c,addr=0x3F,elecvolt=0x20,regratio=0x03,invX=False,invY=False,invdisp=False):
        self.i2c=i2c
        self.slvAddr=addr
        initCMDList=[
            SOFT_RST,
            SET_BOOST,
            0x00,
            SET_BIAS|0x00,
            REGU_RATIO|regratio,
            EVSET_MODE,
            elecvolt,
            SEG_DIR|(0x01 if invX else 0x00),
            COM_DIR|(0x08 if invY else 0x00),
            INV_DISP|(0x01 if invdisp else 0x00),
            SRTLIN_SET|0x00,
            POWER_CTRL|0x04,
            POWER_CTRL|0x06,
            POWER_CTRL|0x07,
            DISP_ONOFF|0x01,
            ALL_PIX_ON]
        self.buffer=bytearray(128*64//8)
        super().__init__(self.buffer, 128, 64, framebuf.MONO_VLSB)
        self.writeCMDL(initCMDList)
        
    def writeCMDL(self,cmdList):
        buff=[]
        for each in cmdList:
            buff.append(0x80)
            buff.append(each)
        buff[-2]=0x00
        self.i2c.writeto(self.slvAddr,bytearray(buff))
    
    def writeData(self,data):
        buff=bytearray([])
        for each in data:
            buff.append(0xC0)
            buff.append(each)
        buff[len(buff)-2]=0x40
        self.i2c.writeto(self.slvAddr,buff)
    
    """def writeCMD(self,cmd):
        buff=[0x00,cmd]
        self.i2c.writeto(self.slvAddr,bytearray(buff))"""
    
    def show(self):
        for pagcnt in range(8):
            self.writeCMDL([SRTLIN_SET|0x00,PAGEAD_SET|pagcnt,COLHAD_SET|0x00,COLLAD_SET|0x00])
            self.writeData(self.buffer[(128*pagcnt):(128*pagcnt+128)])
