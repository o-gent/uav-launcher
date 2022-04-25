import logging
import math
import time

import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter, dump_errors

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, [%(levelname)s], %(module)-5s, %(message)s",
    handlers=[
        logging.FileHandler(f"logs/log_launcher_{time.strftime('%Y%m%d-%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

class Catapult:
    """ abstract odrive functionality for launching things """
    
    def __init__(self, instance=None):
        self.catapult_length = 1.87 # m
        self.radius = 0.0287 # m
        self.cell_no = 10
        self.circumference = 2*math.pi*self.radius

        print("finding an odrive...")
        if instance:
            self.drive = instance
        else:
            self.drive = odrive.find_any()

        self.axis = self.drive.axis1

        print(self.drive)

        print(f"Bus voltage is {self.drive.vbus_voltage} V")
        print(f"{self.drive.vbus_voltage/self.cell_no}V per cell")
        
        self.axis.motor.config.current_lim = 80

        if not self.axis.motor.is_calibrated:
            self.calibrate()

        self.logger = logging.getLogger("main")


    def first_time_setup(self):
        self.axis.motor.config.pole_pairs = 7
        self.axis.motor.config.torque_constant = 8.27/150
        self.axis.encoder.config.cpr = 8192
        self.drive.config.enable_brake_resistor = True
        self.axis.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
        self.axis.motor.config.calibration_current = 5
        self.drive.config.dc_max_positive_current = 100
        self.drive.config.dc_max_negative_current = -20


    def set_speed(self, speed, ramp):
        self.axis.controller.config.vel_limit = 1000
        self.axis.controller.config.vel_ramp_rate = ramp
        self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_VEL_RAMP
        self.axis.controller.input_vel = speed/self.circumference


    def set_location(self, distance):
        """ move the tab to a location relative to the origin """
        # set to a low speed for the reset
        self.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
        self.axis.controller.config.vel_limit = 5
        self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.axis.controller.input_pos = distance/self.circumference


    def idle(self):
        self.axis.requested_state = AXIS_STATE_IDLE


    def calibrate(self):
        print("starting calibration...")
        self.axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)


    def launch(self, speed, ramp):
        location = 0
        self.set_speed(speed, ramp)
        while self.axis.encoder.pos_estimate < self.catapult_length/self.circumference:
            position = format(self.axis.encoder.pos_estimate*self.circumference, '.3f').zfill(5)
            velocity = format(self.axis.encoder.vel_estimate*self.circumference, '.3f').zfill(6)
            current = format(self.axis.motor.current_control.Iq_measured, '.3f').zfill(7)
            mechpower = format(self.axis.controller.mechanical_power, '.3f').zfill(8)
            power = format(self.axis.controller.electrical_power, '.3f').zfill(8)
            rpm = format(self.axis.encoder.vel_estimate*60, '.3f').zfill(8)
            self.logger.info(f"""position:{position}, velocity: {velocity}, current: {current}, mechpower:{mechpower}, power:{power}, rpm:{rpm}""")
        self.set_speed(0, 5)
        dump_errors(self.drive)
        time.sleep(2)
