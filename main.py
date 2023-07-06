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
config.read("config.ini")
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
def getNodeType():
    return config['NODEINFO']['NODETYPE']
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
def readFromULT_3040(serialPort):
    serialPort.serial.baudrate = 9600				# BaudRate
    serialPort.serial.bytesize = 8					# Number of data bits to be requested
    serialPort.serial.parity = minimalmodbus.serial.PARITY_NONE	# Parity Setting here is NONE but can be ODD or EVEN
    serialPort.serial.stopbits = 1					# Number of stop bits
    serialPort.serial.timeout  = 0.1					# Timeout time in seconds
    serialPort.mode = minimalmodbus.MODE_RTU				# Mode to be used (RTU or ascii mode)
    # Good practice to clean up before and after each execution
    serialPort.clear_buffers_before_each_transaction = True
    serialPort.close_port_after_each_call = True
    return serialPort.read_register(2,0,4)
def readFromFromRD_SMT_P_O(serialPort):
    serialPort.serial.baudrate = 9600  # baudrate
    serialPort.serial.bytesize = 8
    serialPort.serial.parity   = serial.PARITY_NONE
    serialPort.serial.stopbits = 1
    serialPort.serial.timeout  = 0.1      # seconds
    serialPort.address         = 1        # this is the slave address number
    serialPort.mode = minimalmodbus.MODE_RTU # rtu or ascii mode
    serialPort.clear_buffers_before_each_transaction = True
    return serialPort.read_register(registeraddress=0,number_of_decimals=1,functioncode=3,signed=True),serialPort.read_register(registeraddress=1,number_of_decimals=1,functioncode=3,signed=True)
def readHumiditySensors(ports):
    sensorList = []
    for port in ports:
        try:
            portcon = minimalmodbus.Instrument(port=port, slaveaddress=1, debug=False)  # port name, slave address (in decimal)
            sensorList.append(portcon)
        except:
            pass
    sensorResponse = {}
    sensorID = 0
    for sensor in sensorList:
        sensorID += 1
        tempature,humidity = readFromFromRD_SMT_P_O(sensor)
        array = [str(arr[0]/10)+"%",str((((arr[1]/1000)*120)-40))]
        sensorResponse["Sensor"+str(sensorID)] = array
    return sensorResponse
def readDistanceSensors(ports):
    sensorList = []#Düzeltilecek
    for port in ports:
        try:
            portcon = minimalmodbus.Instrument(port=port, slaveaddress=1, debug=False)  # port name, slave address (in decimal)
            sensorList.append(portcon)
        except:
            pass
    sensorResponse = {}
    sensorID = 0
    for sensor in sensorList:
        sensorID += 1
        data = readFromULT_3040(sensor)
        sensorResponse["Sensor"+str(sensorID)] = data
    return sensorResponse
if __name__ == '__main__':
    ports = filter(lambda x: 'ttyUSB' in x, serial_ports())
    if (getNodeType() == "2"):
        sensorResponse = readDistanceSensors(ports)
    elif (getNodeType() == "1"):
        sensorResponse = readHumiditySensors(ports)
    else:
        print("Wrong option")
    if len(sensorResponse) != 0:
        nodeName = getNodeName()
        appendData(nodeName, sensorResponse)
