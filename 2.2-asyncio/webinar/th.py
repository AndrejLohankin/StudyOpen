import threading


def some_task():
    return print(2 + 2)


tread = threading.Thread(target=some_task)

tread.start()

tread.join()
