from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os

class NewFileHandler(PatternMatchingEventHandler):
        ignore_directories = True
        patterns = ['*']
        ignore_patterns = []
        case_sensitive = True

        def __init__(self, event_handler):
            self.event_handler = event_handler

        def on_created(self, event):
            self.event_handler(event)
        




class DirectoryObserver:
    def __init__(self, dir) -> None:
        self.dir = dir

    def start_observing(self, handler) -> None:

        """Start observing changes in source folder to handle changes"""

        event_handler = NewFileHandler(handler)
        self.observer = Observer()
        self.observer.schedule(event_handler, path=self.dir, recursive=False)
        self.observer.start()

    def stop_observing(self) -> None:

        """Terminate observing for changes in source folder"""

        self.observer.stop()
            