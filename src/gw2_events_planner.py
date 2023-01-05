import sys
import json
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PyQt6.QtCore import Qt


# Define a function that takes the frequency and minute as input and returns the next occurrence time


def handler(event, context):
    """Lambda entry point"""
    # Create a list of events
    events = get_events()

    # Sort the list of events by next_occurrence
    events.sort(key=lambda event: event.next_occurrence)
    print([dict(event) for event in events])


def hour_minutes(td):
    """Breakdown timedelta into hours and minutes"""
    return td.seconds // 3600, (td.seconds // 60) % 60


def determine_next_occurence(event):
    """Determine the next occurence based on the first occurence of the day and the period"""

    now = datetime.now()
    event_first_occurence = datetime.strptime(event["first_spawn"], "%H:%M")
    # setting up the first occurence of the day
    first_occurence = datetime.now().replace(
        minute=event_first_occurence.minute, hour=event_first_occurence.hour, second=0
    )
    timedelta_between = now - first_occurence
    hours, minutes = hour_minutes(timedelta_between)
    period = int(event["period"])

    last_event = timedelta(hours=hours % period, minutes=minutes)
    delta_to_add = timedelta(hours=period)

    next_occurence = now - last_event + delta_to_add

    return next_occurence


# Define a class that represents an event
class Event:
    def __init__(self, event_detail):
        self.name = event_detail["name"]
        self.first_spawn = event_detail["first_spawn"]
        self.period = event_detail["period"]
        self.next_occurrence = determine_next_occurence(event_detail)

    def __iter__(self):
        yield "name", self.name
        yield "first_spawn", self.first_spawn
        yield "period", self.period
        yield "next_occurrence", self.next_occurrence


def get_events():
    """Return meta-event's metadatas"""
    events = []

    with open("meta.json", "r") as meta_file:
        events_json = json.load(meta_file)
        for e in events_json:
            if e["show"]:
                events.append(Event(e))
    return events


if __name__ == "__main__":
    handler("", "")
