import serial
import serial.tools.list_ports
import glob
import sys
import time
import os
import csv
import glob
from datetime import datetime

# datetime object containing current date and time

 

from pathlib import Path
import configparser
configPath = str(Path.home())+"/Desktop/config.ini"
config = configparser.ConfigParser()
config.read(configPath)
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
        print("hey")
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
            if "USB" in port:  # this part is for linux
                result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    sensorList = []
    ports = serial_ports()
    for port in ports:
        try:
            portcon = serial.Serial(port)
            portcon.timeout = 10
            sensorList.append(portcon)
        except:
            pass
    sensorResponse = {}
    for sensor in sensorList:  # print data from all sensors
        byte = sensor.readline()
        sensorResponse[sensor.name] = byte.decode().replace("\n", "").replace("\r","")
    nodeName = getNodeName()
    appendData(nodeName, sensorResponse)
