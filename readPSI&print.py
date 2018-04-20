
# Read existing values on PSI Board
# mostly taken from J.Bower Ser_Interface_PSI.py

import serial
import time
import csv
import os


def initialize_serialport():
    global ser
    ser = serial.Serial(port='/dev/ttyUSB0',
               baudrate = 57600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1)

### routine to write a string to PSI board
def write_to_PSI(sendCommand):
    ser.write((sendCommand).encode('utf-8')) #removed CR LF as PSI board doesnt seem to need them`

### routine to read a line (up to CR LF) from PSI board
### need to figure out how to deal wht the extra '>' prompt character that 
###   gets sent for some responses
def listen_to_PSI():
    ser_bytes = ser.readline()
    decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode('utf-8')
    return decoded_bytes

### routine to turn logging mode ON if OFF 
def turnLoggingON():
    print("turning on logging")
    write_to_PSI('l')
    output = listen_to_PSI()
    if output == 'Log Off':
        print("logging was already on... turning it back on")
        write_to_PSI('l')

### routine to turn logging mode OFF if ON 
def turnLoggingOFF():
    print("turning off logging")
    write_to_PSI('l')
    output = listen_to_PSI()
    if output == 'Log On':
        print("logging was already off... turning it back off")
        write_to_PSI('l')

### routine to turn debug mode ON if OFF 
def turnDebugON():
    print("turning on debug")
    write_to_PSI('o')
    output = listen_to_PSI()
    print("debug on:", output)
    goofything = ser.read() # just read a character to get rid of the '>'
#    print(goofything)
    time.sleep(0.1)
    if output == 'Debug Off':
        print("Debug was already on... turning it back on")
        write_to_PSI('o')
        output = listen_to_PSI()
        print("debug on:", output)
        goofything = ser.read() # just read a character to get rid of the '>'

### routine to read contents of flash page
### ASSUMES PSI is in Debug Mode ON
def readFlashPage(page):
 #   print("reading page", page)
    write_to_PSI('f')
    output = listen_to_PSI()
    if output == 'Page To Read:':
        write_to_PSI(page)
        flash = listen_to_PSI() #PSI echos back the input
  #      print('flash =',flash)
        heading = listen_to_PSI() # the header CONTENTS:
 #       print(heading)
        contents = listen_to_PSI() # the actual flash page contents
 #       print(contents)
        goofything = ser.read() # just read a character to get rid of the '>'
#        print(goofything)
        list.append(contents)
        print(flash + " = " + contents)
        

### create a list
list=[]

### here is where the main loop starts
def main():
    initialize_serialport()
    ser.reset_input_buffer()
 #   turnLoggingOFF() # make sure logging is not running
    turnDebugON()
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('00')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('01')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('02')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('03')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('04')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('05')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('06')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('07')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('08')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('09')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('0A')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('0B')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('0C')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('0D')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('0E')
    
    time.sleep(0.5) # just to let the PSI board catch its breath
    readFlashPage('0F')
    
    print(list)
    
 #   turnDebugOFF()
    ser.close()




# python bit to figure how who started this
if __name__ == "__main__":
    main()
