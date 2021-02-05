#!/usr/bin/env python
from exchange import get_exchange


class Task:
    def __init__(self, label):
        self.label = label

    def send(self, msg):
        print(self.label, msg)


if __name__ == "__main__":
    task_a = Task("task_a")
    task_b = Task("task_b")

    exc_name = get_exchange("name")
    exc_uname = get_exchange("uname")
    exc_name.attach(task_a)
    exc_name.attach(task_b)
    exc_name.send("msg1")
    exc_name.detach(task_a)
    exc_name.send("msg2")
    exc_uname.send("msg3")
