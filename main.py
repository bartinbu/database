#!/usr/bin/python
import serial
import serial.tools.list_ports
import glob
import sys
import minimalmodbus
import os
import csv
import glob
from datetime import datetime


from pathlib import Path
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")
'''
config = configparser.ConfigParser()
config.add_section('NODEINFO')
config['NODEINFO']['NODENAME'] = "TryZone"
config['NODEINFO']['SENSORSIZE'] = "5"
with open(configPath, 'w+') as configfile:
  config.write(configfile)
'''


def getNodeName():
    return config['NODEINFO']['NODENAME']


def getSensorSize():
    return config['NODEINFO']['NODENAME']


def appendData(nodeName, sensorResponse):
    arr = os.listdir()
    if nodeName not in arr:
        os.mkdir(nodeName)
    
    if not os.path.exists(nodeName+'/data.csv'):
        header = ['Time']
        for key in sensorResponse:
            header.append(key)
        with open(nodeName+'/data.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    row = []
    row.append(datetime.now())
    for key in sensorResponse:
        row.append(sensorResponse[key])
    with open(nodeName+'/data.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
def readFromFromRD_SMT_P_O(serialPort):
    serialPort.serial.baudrate = 9600  # baudrate
    serialPort.serial.bytesize = 8
    serialPort.serial.parity   = serial.PARITY_NONE
    serialPort.serial.stopbits = 1
    serialPort.serial.timeout  = 0.1      # seconds
    serialPort.address         = 1        # this is the slave address number
    serialPort.mode = minimalmodbus.MODE_RTU # rtu or ascii mode
    serialPort.clear_buffers_before_each_transaction = True
    return client1.read_registers(registeraddress=0,number_of_registers=2,functioncode=3)



if __name__ == '__main__':
    sensorList = []
    ports = filter(lambda x: 'ttyUSB' in x, serial_ports())  
    for port in ports:
        try:
            portcon = client1 = minimalmodbus.Instrument(port=port, slaveaddress=1, debug=False)  # port name, slave address (in decimal)
            sensorList.append(portcon)
        except:
            pass
    sensorResponse = {}
    for sensor in sensorList:
        arr = readFromFromRD_SMT_P_O(sensor)
        sensorResponse[sensor.serial.name] = arr
    nodeName = getNodeName()
    appendData(nodeName, sensorResponse)




