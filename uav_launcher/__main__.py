import argparse
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument("speed", type=int, help="exit speed of the catapult")
parser.add_argument("ramp", type=int, help="ramp rate")
parser.add_argument("delay", type=int, help="amount of time in seconds before launching")
parser.add_argument('--setup', action='store_true', help="for first time setup of relevant variables")
parser.add_argument('--path', action='store', type=str, help="process log files to csv")
args, unknown = parser.parse_known_args()
print(args)
print(unknown)

if args.path:
    from uav_launcher.data_process import process_catapult_file
    import os
    import pandas as pd
    for file in os.listdir(args.path):
        p = process_catapult_file(args.path + "/" + file)
        p.to_csv(args.path + "/" + file + ".csv")
    sys.exit()

from uav_launcher.catapult import Catapult

catapult = Catapult()

if args.setup:
    catapult.first_time_setup()
    print("Restart the odrive and don't use -s on the next run")
    sys.exit()

catapult.logger.critical(f"launching at {args.speed} with {args.ramp} ramp rate, in {args.delay} seconds")

time.sleep(args.delay)

catapult.launch(args.speed, args.ramp)

input("press enter to reset catapult")

catapult.set_location(0)
