# Learned it here...
# https://www.devdungeon.com/content/gui-programming-python
# https://pyinmyeye.blogspot.com/2012/08/tkinter-menubutton-demo.html

# first import message box stuff
import tkinter
from tkinter import Tk, Label, Y, LEFT, RIGHT, Button

# then pull data from text document "values.txt"

#OPEN FILE TO BE READ
myFile = open('values.txt', 'r')
listoflines = myFile.read().splitlines()

#Laser DC Setpoint read from values.txt
aline = listoflines[0]
lineitems = aline.split('=')
ldcs = lineitems[1]
#print("Laser DC Setpoint")
#print (ldcs)

#Laser temperature setpoint read from values.txt
aline1 = listoflines[1]
lineitems1 = aline1.split('=')
lts = lineitems1[1]
#print ("Laser Temperature")
#print (lts)

#Laser AC setpoint read from values.txt
aline2 = listoflines[2]
lineitems2 = aline2.split('=')
lacs = lineitems2[1]
#print ("Laser AC setpoint")
#print (lacs)

#Laser Tuning Rate read from values.txt
aline3 = listoflines[3]
lineitems3 = aline3.split('=')
ltr = lineitems3[1]
#print ("Laser Tuning Rate")
#print (ltr)

#Laser Calibration Constant read from values.txt
aline4 = listoflines[4]
lineitems4 = aline4.split('=')
lcc = lineitems4[1]
#print ("Laser Calibration Constant")
#print (lcc)
#
#Laser Temperature DAC Offset read from values.txt
aline5 = listoflines[5]
lineitems5 = aline5.split('=')
ltdo = lineitems5[1]
#print ("Laser Temperature DAC Offset")
#print (ltdo)

#Concentration Offset read from values.txt
aline6 = listoflines[6]
lineitems6 = aline6.split('=')
co = lineitems6[1]
#print ("Concentration Offset")
#print (co)

#Photo Current Monitor Threshold read from values.txt
aline7 = listoflines[7]
lineitems7 = aline7.split('=')
pcmt = lineitems7[1]
#print ("Photo Current Monitor Threshold")
#print (pcmt)

#Current Shutdown Record read from values.txt
aline8 = listoflines[8]
lineitems8 = aline8.split('=')
csr = lineitems8[1]
#print ("Current Shutdown Record")
#print (csr)

#Serial Number read from values.txt
aline9 = listoflines[9]
lineitems9 = aline9.split('=')
sn = lineitems9[1]
#print ("Serial Number")
#print (sn)

#Modulator Gain read from values.txt
aline10 = listoflines[10]
lineitems10 = aline10.split('=')
mg = lineitems10[1]
#print ("Modulator Gain")
#print (mg)

#F2 Correction for I read from values.txt
aline11 = listoflines[11]
lineitems11 = aline11.split('=')
f2cfi = lineitems11[1]
#print ("F2 Modulator for I")
#print (f2cfi)

#F2 Correction for Q read from values.txt
aline12 = listoflines[12]
lineitems12 = aline12.split('=')
f2cfq = lineitems12[1]
#print ("F2 Modulator for Q")
#print (f2cfq)

#Minimum F1 read from values.txt
aline13 = listoflines[13]
lineitems13 = aline13.split('=')
mf1 = lineitems13[1]
#print ("Minimum F1")
#print (mf1)

#Minimum F2 read from values.txt
aline14 = listoflines[14]
lineitems14 = aline14.split('=')
mf2 = lineitems14[1]
#print ("Minimum F2")
#print (mf2)

#Startup Lockout read from values.txt
aline15 = listoflines[15]
lineitems15 = aline15.split('=')
sl = lineitems15[1]
#print ("Startup Lockout")
#print (sl)

##########################################################################################
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


###############################################################################

# Display current existing PSI Board Settings.

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#print("Screen width:", screen_width)
#print("Screen height:", screen_height)

#Center on screen

w = 350 # width for the Tk root
h = 600 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# Title tk box
root.title("EXISTING Values on PSI Board")

# Create a label as a child of root window
my_text = Label(root,justify=LEFT, text=
                
                'Laser DC Setpoint = '+ list[0]
              + '\n\nLaser temperature setpoint = '+ list[1]
              + '\n\nLaser AC setpoint = '+ list[2]
	      + '\n\nLaser Tuning Rate = '+ list[3]
              + '\n\nLaser Calibration Constant = '+ list[4]
	      + '\n\nLaser Temperature DAC Offset = '+ list[5]
	      + '\n\nConcentration Offset = '+ list[6]
	      + '\n\nPhoto Current Monitor Threshold = '+ list[7]
	      + '\n\nCurrent Shutdown Record = '+ list[8]
	      + '\n\nSerial Number = '+ list[9]
	      + '\n\nModulator Gain = '+ list[10]
	      + '\n\nF2 Correction for I = '+ list[12]
	      + '\n\nF2 Correction for Q = '+ list[13]
	      + '\n\nMinimum F1 = '+ list[14]
	      + '\n\nMinimum F2 = '+ list[15]
	      + '\n\nStartup Lockout = '+ list[16])

my_text.config(font=('helvetica', 10))
my_text.pack(padx=5, pady=5)

# Understood
Understood_button = Button(root, text='understood', command=root.destroy)
understood_button.pack()

root.mainloop()



##################################################################################


#now display data to be WRITTEN to board with option to continue or cancel.

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#print("Screen width:", screen_width)
#print("Screen height:", screen_height)

#Center on screen

w = 350 # width for the Tk root
h = 600 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# Title tk box
root.title("Values to Write to PSI Board")

# Create a label as a child of root window
my_text = Label(root,justify=LEFT, text=
                
                'Laser DC Setpoint = '+ ldcs
              + '\n\nLaser temperature setpoint = '+ lts
              + '\n\nLaser AC setpoint = '+ lacs
	      + '\n\nLaser Tuning Rate = '+ ltr
              + '\n\nLaser Calibration Constant = '+ lcc
	      + '\n\nLaser Temperature DAC Offset = '+ ltdo
	      + '\n\nConcentration Offset = '+ co
	      + '\n\nPhoto Current Monitor Threshold = '+ pcmt
	      + '\n\nCurrent Shutdown Record = '+ csr
	      + '\n\nSerial Number = '+ sn
	      + '\n\nModulator Gain = '+ mg
	      + '\n\nF2 Correction for I = '+ f2cfi
	      + '\n\nF2 Correction for Q = '+ f2cfq
	      + '\n\nMinimum F1 = '+ mf1
	      + '\n\nMinimum F2 = '+ mf2
	      + '\n\nStartup Lockout = '+ sl)

#my_text.config(font=('times', 10))
my_text.config(font=('helvetica', 10))
my_text.pack(padx=5, pady=5)


# continue writing values to PSI board
continue_button = Button(root, text='Continue Writing Values to PSI Board', command=root.destroy)
continue_button.pack()

# if CANCEL, kill program.
Cancel_button = Button(root, text='Stop to change values', command=quit)
Cancel_button.pack()

root.mainloop()


####################################################################################

# Write new values to PSI Board.

print("continuing to write :) ")
