import odrive
from odrive.enums import *
import time
import math


class Catapult:
    """ abstract odrive functionality for launching things """
    
    def __init__(self):
        self.catapult_length = 1.87 # m
        self.radius = 0.0287 # m
        self.cell_no = 5
        self.circumference = 2*math.pi*self.radius
        
        print("finding an odrive...")
        self.drive = odrive.find_any()
        self.motor = self.drive.axis1
        print(self.drive)

        print(f"Bus voltage is {self.drive.vbus_voltage} V")
        print(f"{self.drive.vbus_voltage/self.cell_no}V per cell")
        
        if not self.motor.motor.is_calibrated:
            self.calibrate()


    def set_speed(self, speed, ramp):
        self.motor.controller.config.vel_limit = 150
        self.motor.controller.config.vel_ramp_rate = ramp
        self.motor.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.motor.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        self.motor.controller.config.input_mode = INPUT_MODE_VEL_RAMP
        self.motor.controller.input_vel = speed/self.circumference


    def set_location(self, distance):
        """ move the tab to a location relative to the origin """
        # set to a low speed for the reset
        self.motor.controller.config.input_mode = INPUT_MODE_POS_FILTER
        self.motor.controller.config.vel_limit = 5
        self.motor.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.motor.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.motor.controller.input_pos = distance/self.circumference


    def idle(self):
        self.motor.requested_state = AXIS_STATE_IDLE


    def calibrate(self):
        print("starting calibration...")
        self.motor.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while self.motor.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)


    def launch(self, speed):
        location = 0
        self.set_speed(speed, 300)
        while self.motor.encoder.pos_estimate < self.catapult_length/self.circumference:
            time.sleep(0.01)
        self.set_speed(0, 2)
        time.sleep(2)