from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileCreatedEvent
from typing import TypeVar, Callable

T = TypeVar('T')


class NewFileHandler(PatternMatchingEventHandler):
    ignore_directories: bool = True
    patterns: list[str] = ['*']
    ignore_patterns: list[str] = []
    case_sensitive: bool = True

    def __init__(self, event_handler: Callable[[FileCreatedEvent], T]) -> None:
        self.event_handler = event_handler

    def on_created(self, event: FileCreatedEvent) -> T:
        return self.event_handler(event)

    def on_moved(self, event: FileCreatedEvent) -> T:
        return self.event_handler(event)


class DirectoryObserver:
    def __init__(self, dir: str) -> None:
        self.dir = dir

    def start_observing(self, handler: Callable[[FileCreatedEvent], T]) -> None:

        """Start observing changes in source folder to handle changes"""

        event_handler = NewFileHandler(handler)
        self.observer = Observer()
        self.observer.schedule(event_handler, path=self.dir, recursive=False)
        self.observer.start()

    def stop_observing(self) -> None:

        """Terminate observing for changes in source folder"""

        self.observer.stop()
