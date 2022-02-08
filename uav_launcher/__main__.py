import argparse
import time
from uav_launcher.catapult import Catapult

parser = argparse.ArgumentParser()
parser.add_argument("speed", type=int, help="exit speed of the catapult")
parser.add_argument("delay", type=int, help="amount of time in seconds before launching")
args = parser.parse_args()

catapult = Catapult()

print(f"launching at {args.speed} in {args.delay} seconds")
time.sleep(args.delay)

catapult.launch(args.speed)

input("press enter to reset catapult")

catapult.set_location(0)
