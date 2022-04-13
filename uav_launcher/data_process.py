import pandas as pd
from datetime import datetime

def process_catapult_file(file:str):
    store = []
    store.append(["time", "position", "velocity", "current", "rpm"])
    with open(file) as f:
        for line in f.readlines():
            line_list = line.split(",")

            time = datetime.strptime(line_list[0]+"."+line_list[1]+"000", "%Y-%m-%d %H:%M:%S.%f")
            position = float(line_list[4].split(":")[1])
            velocity = float(line_list[5].split(":")[1])
            current = float(line_list[6].split(":")[1])
            rpm = float(line_list[9].split(":")[1])

            store.append([time, position, velocity, current, rpm])
    return pd.DataFrame(store)
