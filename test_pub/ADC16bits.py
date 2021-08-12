#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import rospy
from std_msgs.msg import Float64MultiArray
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

GAIN = 1
sps = 860
sensorValues = [0] * 2

class ADCNode(object):
    def __init__(self, name):
        self.name = name
        rospy.init_node(self.name)
        self.rate = rospy.Rate(1)
        self.initPublishers()
        self.initVariables()
        return

    def initPublishers(self):
        self.ADCPub = rospy.Publisher("/ADC", Float64MultiArray, queue_size = 10)
        return

    def initVariables(self):
        self.ADCValues = Float64MultiArray()
        return

    def main(self):
        rospy.loginfo("[%s] ADC Node Started OK", self.name)
        while not (rospy.is_shutdown()):
            sensorValues[0] = float(adc.read_adc(0, gain=GAIN, data_rate=sps))
            sensorValues[1] = float(adc.read_adc(1, gain=GAIN, data_rate=sps))
            sensorValues[2] = float(adc.read_adc(2, gain=GAIN, data_rate=sps))
            sensorValues[3] = float(adc.read_adc(3, gain=GAIN, data_rate=sps))
            self.ADCValues.data = sensorValues
            self.ADCPub.publish(self.ADCValues)
        return

if __name__=='__main__':
    ADCManager = ADCNode("ADCManager")
    #ADCManager = pressureSensorsNode("ADCManager")
    ADCManager.main()
