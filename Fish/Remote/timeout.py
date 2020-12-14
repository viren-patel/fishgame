from multiprocessing import Process, Queue

TIMEOUT_PERIOD = 1

def timeout(timeout, method, args):
    """
    Runs the provided method with the given arguments, but times it out after the given number of seconds. 
    A timed out function call returns None.
    """
    return_queue = Queue()
    process = Process(target=timeout_wrapper, args=[return_queue, method, args])
    process.start()
    process.join(timeout)
    process.kill()
    if not return_queue.empty():
        return return_queue.get()
    else:
        return None

def timeout_wrapper(return_queue: Queue, method, args):
    """
    A multiprocessing wrapper for the function being called with a timeout.
    """
    if len(args) == 1:
        return_queue.put(method(args[0]))
    elif len(args) > 1:
        return_queue.put(method(*args))
    else:
        return_queue.put(method())
    return 0