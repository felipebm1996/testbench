#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import RPi.GPIO as GPIO
import time
from std_msgs.msg import Float64

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
pwm = GPIO.PWM(17,50)

class MotorConfiguration(object):
    def __init__(self):
        #self.motorPin = 12


        rospy.init_node('motor_angles_configuration', anonymous = True)
        self.motorPub = rospy.Publisher("/motor_angles", Float64, queue_size = 1, latch = False)
        self.angle =  Float64()
        self.duty = Float64()

        self.duty = 0.0
        self.delay = 0.1
        self.angle = 0.0

    def AngleToDuty(self, angle):
        #duty = float (angle)/18.+2.
        self.duty = (self.angle)/36.0+5.0
        #print self.duty
        return self.duty

    def Process(self):
        self.duty = self.AngleToDuty(self.angle)
        pwm.start(5)
        #time.sleep(3)

        for self.angle in range(5,100,5):
            self.motorPub.publish(self.angle)
            self.duty = self.AngleToDuty(self.angle)
            print(self.duty)
           #GPIO.output(12, True)
            pwm.ChangeDutyCycle(self.duty)
            time.sleep(1)
          #print("Position: {}° -> Duty cycle : {}%".format(pos,duty))
        pwm.stop()
        GPIO.cleanup()

def main():
    new = MotorConfiguration()
    rate = rospy.Rate(200)
    rospy.loginfo("Starting Angle Motor Configuration")
    while not (rospy.is_shutdown()):
        new.Process()
    return

if __name__ == '__main__' :
    try:
        main()
    except Exception as e:
        print(e)
