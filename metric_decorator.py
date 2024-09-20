import time
import threading
import queue

metrics_storage = {}

metrics_queue = queue.Queue()

def metrics_collector(func):
    if func.__name__ not in metrics_storage:
        metrics_storage[func.__name__] = {'calls': 0, 'errors': 0, 'total_time': 0.0}

    def wrapper(*args, **kwargs):
        metrics_storage[func.__name__]['calls'] += 1

        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            metrics_storage[func.__name__]['errors'] += 1
            raise e
        finally:
            execution_time = time.time() - start_time
            metrics_storage[func.__name__]['total_time'] += execution_time

            queue_metrics_for_saving(func.__name__)

        return result

    return wrapper

def get_metrics(func_name):
    if func_name in metrics_storage:
        data = metrics_storage[func_name]
        avg_execution_time = data['total_time'] / data['calls'] if data['calls'] > 0 else 0
        return {
            "Function": func_name,
            "Number of calls": data['calls'],
            "Average execution time": avg_execution_time,
            "Number of errors": data['errors']
        }
    else:
        return "No metrics available for this function"

def queue_metrics_for_saving(func_name):
    metrics = get_metrics(func_name)
    metrics_queue.put((func_name, metrics))

def save_metrics_to_db(save_function):
    while True:
        try:
            func_name, metrics = metrics_queue.get(timeout=5)
            save_function(func_name, metrics)
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error saving metrics: {e}")

def start_saving_thread(save_function):
    thread = threading.Thread(target=save_metrics_to_db, args=(save_function,), daemon=True)
    thread.start()
