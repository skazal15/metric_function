
# Metrics Collector: Asynchronous Function Metrics Collection and Storage

This project provides a Python-based solution to collect, store, and analyze performance metrics for functions in constant time (**O(1)**). Metrics such as the number of function calls, average execution time, and error counts are tracked. The collected metrics are then saved asynchronously to a SQLite database without blocking the main function execution, ensuring high performance.

## Features

- **O(1) Metrics Storage and Retrieval**: The metrics for each decorated function are stored and retrieved in constant time using Python's dictionary structure.
- **Asynchronous Database Saving**: Metrics are queued and saved to a database in the background, ensuring that the main function's execution is not delayed.
- **No Direct Database Access in the Decorator**: The decorator only collects metrics and queues them for asynchronous saving, minimizing latency.
- **Threaded Background Task**: A background thread is used to save the metrics to a database SQLite asynchronously.

## Prerequisites

- **Python 3.6+**
- **SQLite3** (included with Python)
- Alternatively, you can modify the code to use **PostgreSQL** or another database system.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/skazal15/metric_function.git
   cd metrics-collector
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies (if using external packages like `psycopg2` for PostgreSQL):
   ```bash
   pip install sqlite3
   ```

## Project Structure

```
metrics-collector/
│
├── metrics_decorator.py    # Core functionality: collects and queues metrics
├── metrics_db.py           # Handles database operations
├── main.py                 # Example usage of the decorator
└── README.md               # Project documentation
```

## Usage

### 1. Define and Decorate Your Functions

To collect metrics for a function, simply decorate the function with `@metrics_collector`:

```python
from metrics_decorator import metrics_collector

@metrics_collector
def example_function():
    # Simulate some work
    time.sleep(1)
```

### 2. Start the Background Thread for Asynchronous Saving

Before running your decorated functions, start the background thread that processes the metrics and saves them to the database asynchronously:

```python
from metrics_decorator import start_saving_thread
from metrics_db import save_to_db

# Start background thread
start_saving_thread(save_to_db)
```

### 3. Call Your Functions

Once your function is decorated and the thread is running, call your function as normal:

```python
example_function()
example_function()
```

### 4. Retrieve Metrics

You can retrieve the metrics collected for any decorated function in constant time:

```python
from metrics_decorator import get_metrics

# Retrieve metrics for example_function
metrics = get_metrics('example_function')
print(metrics)
```

This will output something like:
```python
{
    'Function': 'example_function',
    'Number of calls': 2,
    'Average execution time': 1.0,
    'Number of errors': 0
}
```

### 5. View Data in the Database

The metrics are asynchronously saved to a SQLite database (`metrics.db`). You can open this file using any SQLite viewer or directly query the database to view stored metrics.

## Example

Here's a complete example (`main.py`) of how to use the metrics collector:

```python
from metrics_decorator import metrics_collector, get_metrics, queue_metrics_for_saving, start_saving_thread
from metrics_db import save_to_db
import time

# Example function to be decorated
@metrics_collector
def example_function():
    time.sleep(1)  # Simulate some work

# Start the background thread to save metrics asynchronously
start_saving_thread(save_to_db)

# Call the function multiple times
example_function()
example_function()

# Retrieve and display metrics
metrics = get_metrics('example_function')
print(metrics)

# Queue the metrics for asynchronous saving to the database
queue_metrics_for_saving('example_function')
```

### Running the Program

1. Ensure you have Python installed.
2. Run the program:
   ```bash
   python main.py
   ```

After execution, the metrics will be printed to the console and stored in `metrics.db`.

### Database Schema

The database stores the following metrics:

| Column        | Type    | Description                                |
| ------------- | ------- | ------------------------------------------ |
| `function_name` | TEXT    | The name of the decorated function          |
| `calls`         | INTEGER | The total number of times the function was called |
| `average_time`  | REAL    | The average execution time of the function |
| `errors`        | INTEGER | The total number of errors encountered     |

## Customization

### Using PostgreSQL

If you want to use PostgreSQL instead of SQLite, you can modify `metrics_db.py` to connect to PostgreSQL using a library like `psycopg2`. Install `psycopg2`:

```bash
pip install psycopg2
```

Then modify the connection part in `save_to_db`:

```python
import psycopg2

def save_to_db(func_name, metrics):
    conn = psycopg2.connect(
        dbname='your_db',
        user='your_user',
        password='your_password',
        host='your_host'
    )
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        function_name TEXT PRIMARY KEY,
        calls INTEGER,
        average_time REAL,
        errors INTEGER
    )
    ''')

    cursor.execute('''
    INSERT INTO metrics (function_name, calls, average_time, errors)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (function_name)
    DO UPDATE SET calls=%s, average_time=%s, errors=%s
    ''', (func_name, metrics['Number of calls'], metrics['Average execution time'], metrics['Number of errors'],
          metrics['Number of calls'], metrics['Average execution time'], metrics['Number of errors']))

    conn.commit()
    conn.close()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
