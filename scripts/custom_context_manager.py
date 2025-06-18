from contextlib import contextmanager
import time

@contextmanager
def code_timer(name: str):
    """
    A context manager that times the execution of a block of code.

    Args:
        name (str): The name of the code block being timed.

    Yields:
        None
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"{name} took {elapsed_time:.4f} seconds to execute.")

if __name__ == '__main__':
    # Example usage of the custom context manager
    # This will time the execution of the code block within the context manager
    # and print the elapsed time.

    # For demonstration, we can use a simple loop or any other code block.

    print(f'started custom context manager script')
    with code_timer('pobieranie danych z API'):
        time.sleep(1)

    print(f'przetwarzanie obrazu dockera')
    with code_timer('przetwarzanie obrazu'):
        time.sleep(1)
