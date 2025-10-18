import sys
import threading
import time

def cpu_bound_task():
    """A simple CPU-intensive task."""
    result = 0
    for _ in range(10**7):
        result += 1
    return result

if __name__ == "__main__":
    print(f"Is GIL enabled? {sys._is_gil_enabled()}")

    start_time = time.perf_counter()

    # Create and start multiple threads for the CPU-bound task
    threads = []
    for _ in range(4):  # Example with 4 threads
        thread = threading.Thread(target=cpu_bound_task)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()
    print(f"Execution time with multiple threads: {end_time - start_time:.2f} seconds")

    # For comparison, run the task sequentially
    start_time_seq = time.perf_counter()
    for _ in range(4):
        cpu_bound_task()
    end_time_seq = time.perf_counter()
    print(f"Execution time with sequential calls: {end_time_seq - start_time_seq:.2f} seconds")