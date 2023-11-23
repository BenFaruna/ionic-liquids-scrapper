#!/usr/bin/env python
# -*- coding: utf-8 -*-
from csv import DictWriter
from queue import Queue

def write_to_file(data: list) -> None:

    headers = [
        "SetID", "Reference", "Property", "Phase(s)",
        "Component 1", "Component 2", "Component 3",
        "Datapoints", "Name 1", "Name 2", "Name 3"
    ]

    with open("./ionic_liquids.csv", "a", encoding="utf-8") as f:
        writer = DictWriter(f, headers)
        writer.writerows(data)


def thread_function(q: Queue) -> None:
    print("Thread started...")

    while True:
        if q.empty():
            continue

        data = q.get()
        if data:
            write_to_file(data)
        else:
            break

    print("Thread ended!!!")
