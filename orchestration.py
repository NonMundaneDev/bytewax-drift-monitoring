
from datetime import datetime, timedelta, timezone

import operator
from bytewax.testing import TestingInput
from datetime import timedelta, datetime, timezone
from app.dashboard import generate_dashboard
from bytewax.inputs import DynamicInput, StatelessSource
from bytewax.dataflow import Dataflow
from bytewax.connectors.stdio import StdOutput
from bytewax.window import SystemClockConfig, SlidingWindow,TumblingWindow,EventClockConfig
from bytewax.connectors.files import FileInput, CSVInput
import pandas as pd
from datetime import datetime, timedelta, timezone


# Define a function to accumulate data into lists per window
def data_values(acc, data):
    acc.append(data)
    return acc

# Instantiate the Bytewax Dataflow
flow = Dataflow()

# Read reference dataset CSV file 
flow.input("reference dataset", CSVInput("app/data/inference_data.csv")) 



def parse_time(data):
    data["id"] = datetime.fromtimestamp(float(data["id"]), timezone.utc)
    return data

flow.map(parse_time)

# Map data to tuples containing label 
flow.map(lambda data: (data['label'], data))

def get_time(data):
    return data["id"]

# Configure windowing using SystemClock and TumblingWindow
clock_config = EventClockConfig(get_time, wait_for_system_duration=timedelta(seconds=30))
window_config = TumblingWindow(length=timedelta(minutes=3), align_to=datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0))

# Fold data into windows by label, accumulating lists
flow.fold_window("sum", clock_config, window_config, list, data_values)

# Generate data drift report for each window
flow.map(generate_dashboard)

# Write drift report to standard output
flow.output("out", StdOutput())  

