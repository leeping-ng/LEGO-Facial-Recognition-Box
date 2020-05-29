import time
import RPi.GPIO as GPIO


def init_servo():
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

    # start running PWN on pin and sets it to 0
    pwm.start(0)

def rotate_servo(angle):
    
    duty_cycle = angle/30.0 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()
