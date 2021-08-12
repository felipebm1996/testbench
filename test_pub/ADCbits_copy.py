#!/usr/bin/env python3
import time
import board
import rospy
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from std_msgs.msg import Float64
#import Adafruit_ADS1x15

#adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

GAIN = 1
sps = 860
sensorValues = [0] * 2

class ADCNode(object):
    def __init__(self, name):
        self.name = name
        rospy.init_node(self.name)
        self.rate = rospy.Rate(1)
        self.initPublishers()
        return

    def initPublishers(self):
        self.ADCPub = rospy.Publisher("/ADC", Float64, queue_size = 10)
        return

    def main(self):
        i2c =busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        counter = 0
        rospy.loginfo("[%s] ADC Node Started OK", self.name)
        while not (rospy.is_shutdown()):
            chan0 = AnalogIn(ads,ADS.P0)
            chan0 = chan0.value
            #chan1 = AnalogIn(ads,ADS.P1)
             
            #sensorValues[0] = float(adc.read_adc(0, gain=GAIN, data_rate=sps))
            #sensorValues[1] = float(adc.read_adc(1, gain=GAIN, data_rate=sps))
            #sensorValues[2] = float(adc.read_adc(2, gain=GAIN, data_rate=sps))
            #sensorValues[3] = float(adc.read_adc(3, gain=GAIN, data_rate=sps))
            self.ADCPub.publish(chan0)
        return

if __name__=='__main__':
    try:
        rospy.loginfo("publishing angle joint..")
        ADCManager = ADCNode("ADCManager")
        ADCManager.main()
    except IOError as e:
        print(e)
