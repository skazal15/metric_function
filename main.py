from metric_decorator import metrics_collector, get_metrics, queue_metrics_for_saving, start_saving_thread
from metric_db import save_to_db
import time

@metrics_collector
def example_function():
    time.sleep(1)

start_saving_thread(save_to_db)

example_function()
example_function()

metrics = get_metrics('example_function')
print(metrics)

queue_metrics_for_saving('example_function')
