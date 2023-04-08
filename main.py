import visa
import time
from datetime import datetime
import os

now = datetime.now()
print(now)
fT = open('/Users/TSD/Google Drive/share-TSD/TSD-VISA/TSD-T.txt', 'w+')
fT.write(str(now))
fT.write("\n")
fT.close()
fI = open('/Users/TSD/Google Drive/share-TSD/TSD-VISA/TSD-I.txt', 'w+')
fI.write(str(now))
fI.write("\n")
fI.close()
rm = visa.ResourceManager()
print(rm.list_resources())

dev1 = rm.open_resource('GPIB0::9::INSTR')  #dev1=34970a
dev2 = rm.open_resource('GPIB0::1::INSTR')  #dev2=6430


# test communication with dev1&dev2
print(dev1.query('*IDN?'))
print(dev2.query('*IDN?'))

# funciton1: set conditions
PreC=int(input('Please type "1" to set the condition'
                       ' or "0" to keep pre-set conditions'
               '(Interval = 5, Max-T= 300 C) or "2" for fast test:'))
if PreC == 1:
    Interval=int(input('please input Interval:'))
    MaxTemperature=int(input('please input Max temperature:'))
elif PreC == 0:
    Interval = 5
    MaxTemperature = 300
elif PreC == 2:
    Interval = 10
    MaxTemperature = 21
else:
    print ('Please input correct number')


N=(MaxTemperature-20)*60/Interval  # number of measurement

print(N)


#2:configuration for dev1&2
dev2.write("*RST")
dev2.write("SOUR:FUNC VOLT")
dev2.write("SOUR:VOLT:MODE FIX")
dev2.write("SOUR:VOLT:RANG 0.2")
dev2.write("SOUR:VOLT:LEV 0")
dev2.write("SENS:FUNC 'CURR'")
dev2.write("SENS:CURR:PROT 10e-8")
dev2.write("SENS:CURR:RANG 10e-12")
dev2.write("FORM:ELEM:SENS CURR")
dev2.write("OUTP ON")

dev1.write("*RST")
dev1.write("SYST:DATE 2011,07,24")  # set the time
dev1.write("SYST:TIME 00,00,00")
dev1.write("CONF:TEMP TC,K,(@101)")
dev1.write("ROUT:SCAN (@101)")
#dev1.write("ROUT:MON:CHAN (@101)")
dev1.write("ROUT:MON:STAT ON")
dev1.write("FORM:READ:UNIT OFF")
dev1.write("FORM:READ:TIME:TYPE ABS")
dev1.write("FORM:READ:TIME ON")

time.sleep(3)   # wait for reaction
# 3:get data

fT = open('/Users/TSD/Google Drive/share-TSD/TSD-VISA/TSD-T.txt', 'a')
fI = open('/Users/TSD/Google Drive/share-TSD/TSD-VISA/TSD-I.txt', 'a')

for i in range(N):
    T = dev1.query("READ?")
    print(T)
    dev2.write("READ?")
    time.sleep(1.87)
    I= dev2.read_raw()
    print(I)
    fI.write(str(I))
    fT.write(str(T))
    time.sleep(Interval-2)
    # print(dev2.query('READ?')) timeout error for 6430
    # print(I)

fI.close()
fT.close()

#4 data storage