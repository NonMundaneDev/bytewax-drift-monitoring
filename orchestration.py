# from bytewax.connectors.kafka import KafkaInput
# from bytewax.inputs import DynamicInput, StatelessSource
# from bytewax.connectors.stdio import StdOutput

import operator
from bytewax.testing import TestingInput
from datetime import timedelta, datetime, timezone
from app.dashboard import retrieve_all_data, generate_dashboard,load_reference_data
from bytewax.inputs import DynamicInput, StatelessSource
from bytewax.dataflow import Dataflow
from bytewax.connectors.stdio import StdOutput
from bytewax.window import SystemClockConfig, TumblingWindow
from bytewax.connectors.files import FileInput
# Bytewax has input and output helpers for common input and output data sources
# but you can also create your own with the ManualOutputConfig.

from bytewax.testing import run_main





def count(counts, typ):
    if typ not in counts:
        counts[typ] = 0
    counts[typ] += 1
    return counts




flow = Dataflow()
flow.input("inp", FileInput("DATA_WINDOW_SIZE.txt"))
flow.map(generate_dashboard)

clock_config = SystemClockConfig()
window_config = TumblingWindow(
        length=timedelta(seconds=10), align_to=datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    )
flow.fold_window("count", clock_config, window_config, dict, count)
# flow.reduce_window("sum", clock_config, window_config)
flow.output("out", StdOutput())


if __name__ == "__main__":
    run_main(flow)

