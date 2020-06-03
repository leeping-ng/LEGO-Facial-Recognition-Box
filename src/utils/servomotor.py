import time
import RPi.GPIO as GPIO

def init_servo():
    """
    Setup servo and initialise PWM instance
    """
    servoPIN = 17
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    global pwm
    pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

    # start running PWN on pin and set it to 0
    pwm.start(0)

def rotate_servo(angle):
    """
    Rotate the servo to the given angle
    """
    # Duty cycle calculation: https://medium.com/@rovai/pan-tilt-multi-servo-control-62f723d03f26
    # Values in this equation were obtained by calibrating the servo (see readme)
    duty_cycle = angle/30.0 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)

    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()
