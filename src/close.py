# import RPi.GPIO as GPIO
# import time

# servoPIN = 17
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN, GPIO.OUT)

# pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

# # start running PWN on pin and sets it to 0
# pwm.start(0)

# angle = 0
# duty = angle / 27 +2.5

# # close the box
# pwm.ChangeDutyCycle(duty)
# time.sleep(1)



# # clean up everything
# pwm.stop()
# GPIO.cleanup()

from utils.servo_utils import init_servo, rotate_servo

init_servo()
rotate_servo(0)