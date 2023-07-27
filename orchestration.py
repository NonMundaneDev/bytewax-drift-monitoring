# from bytewax.connectors.kafka import KafkaInput
# from bytewax.inputs import DynamicInput, StatelessSource
# from bytewax.connectors.stdio import StdOutput
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
# Bytewax has input and output helpers for common input and output data sources
# but you can also create your own with the ManualOutputConfig.

from bytewax.testing import run_main
from pydantic import BaseModel, confloat, conint

class PatientData(BaseModel):
    
    diarrhea: conint(ge=0, le=1)
    itchy_nose: conint(ge=0, le=1)
    itchy_eyes: conint(ge=0, le=1)  
    itchy_mouth: conint(ge=0, le=1)
    itchy_inner_ear: conint(ge=0, le=1) 
    redness_of_eyes: conint(ge=0, le=1)
    label: conint(ge=0, le=1)




def convert_value_str_to_int(data):
    print(data)
    df = pd.DataFrame(data, index=[0])
    df = df.apply(pd.to_numeric, errors='ignore')
    # Convert back to dict
    data = df.to_dict(orient='records')[0]
    return data





def count(counts, typ):
    if typ not in counts:
        counts[typ] = 0
    counts[typ] += 1
    return counts



def data_values(acc, data):
    acc.append(data)
    return acc

flow = Dataflow()
flow.input("reference dataset", CSVInput("app/data/inference_data.csv"))

#reformat to tuple
flow.map(lambda data: (data['label'], data))

clock_config = SystemClockConfig()

window_config = TumblingWindow(
        length=timedelta(minutes=3), align_to=datetime.now(timezone.utc).replace(minute=1, second=0, microsecond=0)
    )
flow.fold_window("sum", clock_config, window_config,list,data_values)

flow.map(generate_dashboard)
flow.output("out", StdOutput())

if __name__== "__main__":
    run_main(flow)

