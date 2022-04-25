# GPIO PINOUT BOARD
MOTOR_ONE_STEP_BOARD = 7
MOTOR_ONE_DIR_BOARD = 8

MOTOR_TWO_STEP_BOARD = 11
MOTOR_TWO_DIR_BOARD = 12

MOTOR_THREE_STEP_BOARD = 15
MOTOR_THREE_DIR_BOARD = 16

MOTOR_FOUR_STEP_BOARD = 37
MOTOR_FOUR_DIR_BOARD = 38

# GPIO PINOUT BCM
MOTOR_ONE_STEP = 4
MOTOR_ONE_DIR = 14

MOTOR_TWO_STEP = 17
MOTOR_TWO_DIR = 18

MOTOR_THREE_STEP = 22
MOTOR_THREE_DIR = 23

MOTOR_FOUR_STEP = 26
MOTOR_FOUR_DIR = 20

MICROSTEP_PINS = (-1, -1, -1)

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from time import sleep


# GPIO.setmode(GPIO.BOARD)

motor_one = RpiMotorLib.A4988Nema(MOTOR_ONE_DIR, MOTOR_ONE_STEP, MICROSTEP_PINS, "A4988")
motor_two = RpiMotorLib.A4988Nema(MOTOR_TWO_DIR, MOTOR_TWO_STEP, MICROSTEP_PINS, "A4988")
motor_three = RpiMotorLib.A4988Nema(MOTOR_THREE_DIR, MOTOR_THREE_STEP, MICROSTEP_PINS, "A4988")
motor_four = RpiMotorLib.A4988Nema(MOTOR_FOUR_DIR, MOTOR_FOUR_STEP, MICROSTEP_PINS, "A4988")
while True:
        motor_one.motor_go(False, "Full" , 200, .00125, False, .05)
        # sleep(2)
        motor_two.motor_go(False, "Full" , 200, .00125, False, .05)
        # sleep(2)
        motor_three.motor_go(False, "Full" , 200, .00125, False, .05)
        # sleep(2)
        motor_four.motor_go(False, "Full" , 200, .00125, False, .05)
        sleep(2)

GPIO.cleanup()